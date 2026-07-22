"""Pure-pandas aggregation: per-category product stats and complaint samples.

No API calls here - this only computes what the prompt needs.
"""

import pandas as pd

from . import config
from .images import build_image_lookup

_image_lookup: dict[str, str] | None = None


def _get_image_lookup() -> dict[str, str]:
    global _image_lookup
    if _image_lookup is None:
        _image_lookup = build_image_lookup(config.RAW_DATA_DIR)
    return _image_lookup


def _product_stats(category_df: pd.DataFrame) -> pd.DataFrame:
    """Per-product avg_rating / review_count / pct_negative for one meta_category."""
    grouped = category_df.groupby("name").agg(
        avg_rating=("reviews.rating", "mean"),
        review_count=("reviews.rating", "count"),
        negative_count=("sentiment", lambda s: (s == "Negative").sum()),
    )
    grouped["pct_negative"] = grouped["negative_count"] / grouped["review_count"]
    return grouped.drop(columns="negative_count")


def _sample_complaints(category_df: pd.DataFrame, product_name: str) -> list[str]:
    """Up to MAX_COMPLAINT_SAMPLES negative review texts for a product (reproducible)."""
    negative_reviews = category_df[
        (category_df["name"] == product_name) & (category_df["sentiment"] == "Negative")
    ]["reviews.text"].dropna()
    sample_size = min(config.MAX_COMPLAINT_SAMPLES, len(negative_reviews))
    if sample_size == 0:
        return []
    return negative_reviews.sample(n=sample_size, random_state=config.RANDOM_SEED).tolist()


def _product_entry(category_df: pd.DataFrame, name: str, row: pd.Series) -> dict:
    return {
        "name": name,
        "avg_rating": round(float(row["avg_rating"]), 2),
        "review_count": int(row["review_count"]),
        "pct_negative": round(float(row["pct_negative"]), 3),
        "sample_complaints": _sample_complaints(category_df, name),
        "image_url": _get_image_lookup().get(name),
    }


def build_category_stats(category_df: pd.DataFrame, category_name: str) -> dict:
    """Aggregate one meta_category's reviews into top/worst product stats.

    Filtering to review_count >= MIN_REVIEWS_PER_PRODUCT happens before ranking so a
    product with one 5-star (or one 1-star) review can't take a top/worst slot ahead
    of products with a real track record.
    """
    stats = _product_stats(category_df)
    eligible = stats[stats["review_count"] >= config.MIN_REVIEWS_PER_PRODUCT]

    top_ranked = eligible.sort_values(
        by=["avg_rating", "review_count"], ascending=[False, False]
    ).head(config.TOP_N_PRODUCTS)
    top_products = [
        _product_entry(category_df, name, row) for name, row in top_ranked.iterrows()
    ]

    worst_product = None
    remaining = eligible.drop(index=top_ranked.index).sort_values(by="avg_rating", ascending=True)
    if not remaining.empty:
        worst_name = remaining.index[0]
        worst_product = _product_entry(category_df, worst_name, remaining.iloc[0])

    return {
        "category": category_name,
        "total_reviews": int(len(category_df)),
        "avg_rating": round(float(category_df["reviews.rating"].mean()), 2),
        "pct_negative": round(float((category_df["sentiment"] == "Negative").mean()), 3),
        "top_products": top_products,
        "worst_product": worst_product,
    }
