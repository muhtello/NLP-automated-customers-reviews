"""Product search and per-product review lookup, backed by ml/outputs/cleaned_reviews.parquet.

Loaded once per process (the file is ~50k rows) rather than per-request. Category-aware
ranking (`rank_products`) reads data/reviews_with_meta_categories.csv instead, since that's
the only artifact carrying the meta_category label (see ml/src/summarization/aggregate.py,
whose per-category ranking logic this mirrors).
"""

import random
import re
from functools import lru_cache
from pathlib import Path

import pandas as pd

_REPO_ROOT = Path(__file__).resolve().parents[2]
_ML_OUTPUTS_DIR = _REPO_ROOT / "ml" / "outputs"
_CLEANED_REVIEWS_PATH = _ML_OUTPUTS_DIR / "cleaned_reviews.parquet"
_META_CATEGORY_PATH = _REPO_ROOT / "data" / "reviews_with_meta_categories.csv"

MAX_SEARCH_RESULTS = 30
MAX_REVIEWS_TO_ANALYZE = 300
_SAMPLE_SEED = 42

# Mirrors ml/src/summarization/config.py so chat rankings agree with the dashboard summaries.
MIN_REVIEWS_FOR_RANKING = 5
MAX_RANKING_LIMIT = 20


@lru_cache(maxsize=1)
def _reviews_df() -> pd.DataFrame:
    return pd.read_parquet(_CLEANED_REVIEWS_PATH, columns=["name", "reviews.rating", "reviews.text"])


@lru_cache(maxsize=1)
def _meta_category_df() -> pd.DataFrame:
    return pd.read_csv(_META_CATEGORY_PATH, usecols=["name", "meta_category", "reviews.rating", "sentiment"])


def _slugify(category_name: str) -> str:
    slug = category_name.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


@lru_cache(maxsize=1)
def _category_slug_map() -> dict[str, str]:
    """Dashboard category slug -> raw meta_category label, e.g. 'e-readers-e-books' -> 'E-Readers & E-Books'."""
    categories = _meta_category_df()["meta_category"].dropna().unique()
    return {_slugify(category): category for category in categories}


def search_products(query: str) -> list[dict]:
    df = _reviews_df()
    if query.strip() != "":
        df = df[df["name"].str.contains(query, case=False, na=False, regex=False)]

    grouped = df.groupby("name").agg(
        review_count=("reviews.rating", "count"),
        avg_rating=("reviews.rating", "mean"),
    )
    grouped = grouped.sort_values(by="review_count", ascending=False).head(MAX_SEARCH_RESULTS)

    return [
        {"name": name, "review_count": int(row["review_count"]), "avg_rating": round(float(row["avg_rating"]), 2)}
        for name, row in grouped.iterrows()
    ]


def get_product_reviews(name: str) -> tuple[list[str], int, float]:
    """Returns (sampled review texts capped at MAX_REVIEWS_TO_ANALYZE, total review count, avg rating)."""
    matches = _reviews_df()[_reviews_df()["name"] == name]
    texts = matches["reviews.text"].dropna().tolist()
    total = len(matches)
    avg_rating = round(float(matches["reviews.rating"].mean()), 2) if total > 0 else 0.0

    if len(texts) > MAX_REVIEWS_TO_ANALYZE:
        texts = random.Random(_SAMPLE_SEED).sample(texts, MAX_REVIEWS_TO_ANALYZE)

    return texts, total, avg_rating


def find_product(name: str) -> dict | None:
    """Case-insensitive exact-name lookup, used by the chatbot to confirm a product exists."""
    matches = _reviews_df()
    matches = matches[matches["name"].str.lower() == name.strip().lower()]
    if matches.empty:
        return None

    return {
        "name": matches["name"].iloc[0],
        "review_count": int(len(matches)),
        "avg_rating": round(float(matches["reviews.rating"].mean()), 2),
    }


def get_product_comparison(name: str) -> dict | None:
    """Best- and worst-rated review on file for one product, for a chat side-by-side comparison."""
    matches = _reviews_df()
    matches = matches[matches["name"].str.lower() == name.strip().lower()]
    matches = matches.dropna(subset=["reviews.text"])
    if matches.empty:
        return None

    best = matches.sort_values(by="reviews.rating", ascending=False).iloc[0]
    worst = matches.sort_values(by="reviews.rating", ascending=True).iloc[0]

    return {
        "name": matches["name"].iloc[0],
        "review_count": int(len(matches)),
        "avg_rating": round(float(matches["reviews.rating"].mean()), 2),
        "best_review": {"rating": float(best["reviews.rating"]), "text": best["reviews.text"]},
        "worst_review": {"rating": float(worst["reviews.rating"]), "text": worst["reviews.text"]},
    }


def resolve_category(query: str) -> str | None:
    """Matches a free-text category guess (e.g. 'pets', 'e-readers') to a known dashboard slug.

    Matching is deliberately strict (slug/label word overlap only, no fuzzy/semantic guessing)
    so an unrelated request — e.g. "cat products" when the dataset has no cat-specific
    category — resolves to None instead of silently substituting a different category.
    """
    query_slug = _slugify(query)
    if query_slug == "":
        return None

    query_words = set(query_slug.split("-"))
    for slug, label in _category_slug_map().items():
        if query_slug == slug:
            return slug
        category_words = set(slug.split("-")) | set(_slugify(label).split("-"))
        if query_words & category_words:
            return slug
    return None


def rank_products(category_slug: str | None, order: str, limit: int) -> dict:
    """Top- or bottom-rated products by avg rating, optionally scoped to one dashboard category."""
    df = _meta_category_df()

    category_label = None
    if category_slug is not None:
        category_label = _category_slug_map().get(category_slug)
        if category_label is None:
            return {"category": None, "order": order, "products": []}
        df = df[df["meta_category"] == category_label]

    grouped = df.groupby("name").agg(
        avg_rating=("reviews.rating", "mean"),
        review_count=("reviews.rating", "count"),
        negative_count=("sentiment", lambda s: (s == "Negative").sum()),
    )
    grouped["pct_negative"] = grouped["negative_count"] / grouped["review_count"]
    eligible = grouped[grouped["review_count"] >= MIN_REVIEWS_FOR_RANKING]

    ranked = eligible.sort_values(by="avg_rating", ascending=(order == "worst"))
    ranked = ranked.head(min(max(limit, 1), MAX_RANKING_LIMIT))

    products = [
        {
            "name": product_name,
            "avg_rating": round(float(row["avg_rating"]), 2),
            "review_count": int(row["review_count"]),
            "pct_negative": round(float(row["pct_negative"]), 3),
        }
        for product_name, row in ranked.iterrows()
    ]
    return {"category": category_label, "order": order, "products": products}
