"""Merge the three raw CSVs and produce one cleaned reviews dataset.

Usage:
    python -m src.data_cleaning.pipeline
Run from the `ml/` directory (so the `data/` and `outputs/` paths resolve).
"""

from src.data_cleaning.load import load_all_raw
from src.data_cleaning.clean import (
    clean_name,
    drop_missing_text,
    clean_rating,
    deduplicate,
    add_sentiment_label,
    normalize_whitespace,
)

DATA_DIR = "../data"
OUTPUT_CSV_PATH = "outputs/cleaned_reviews.csv"
OUTPUT_PARQUET_PATH = "outputs/cleaned_reviews.parquet"


def run():
    df = load_all_raw(DATA_DIR)
    print(f"Loaded {len(df)} raw rows from 3 files")

    df = clean_name(df)
    df = drop_missing_text(df)
    df = clean_rating(df)
    df = normalize_whitespace(df)
    df = deduplicate(df)
    df = add_sentiment_label(df)

    print(f"Cleaned dataset: {len(df)} rows, {df['name'].nunique()} unique product names")
    print(df["sentiment"].value_counts(normalize=True).round(3))

    df.to_csv(OUTPUT_CSV_PATH, index=False)
    df.to_parquet(OUTPUT_PARQUET_PATH, index=False)
    print(f"Saved to {OUTPUT_CSV_PATH} and {OUTPUT_PARQUET_PATH}")


if __name__ == "__main__":
    run()
