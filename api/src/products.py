"""Product search and per-product review lookup, backed by ml/outputs/cleaned_reviews.parquet.

Loaded once per process (the file is ~50k rows) rather than per-request.
"""

import random
from functools import lru_cache
from pathlib import Path

import pandas as pd

_ML_OUTPUTS_DIR = Path(__file__).resolve().parents[2] / "ml" / "outputs"
_CLEANED_REVIEWS_PATH = _ML_OUTPUTS_DIR / "cleaned_reviews.parquet"

MAX_SEARCH_RESULTS = 30
MAX_REVIEWS_TO_ANALYZE = 300
_SAMPLE_SEED = 42


@lru_cache(maxsize=1)
def _reviews_df() -> pd.DataFrame:
    return pd.read_parquet(_CLEANED_REVIEWS_PATH, columns=["name", "reviews.rating", "reviews.text"])


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
