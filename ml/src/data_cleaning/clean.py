"""Cleaning steps applied to the merged raw review data."""

import pandas as pd

RATING_TO_SENTIMENT = {
    1: "Negative",
    2: "Negative",
    # 3 (Neutral) is dropped: text at this rating is too ambiguous to serve
    4: "Positive",
    5: "Positive",
}


def clean_name(df):
    # Some `name` values concatenate two unrelated product names, comma-separated.
    # Keeping only the first segment recovers a single real product name.
    df = df.copy()
    df["name"] = (
        df["name"].astype(str).str.split(",").str[0].str.strip().replace("nan", pd.NA)
    )
    return df


def drop_missing_text(df):
    df = df.copy()
    df["reviews.text"] = df["reviews.text"].astype(str).str.strip()
    return df[df["reviews.text"].notna() & (df["reviews.text"] != "") & (df["reviews.text"] != "nan")]


def clean_rating(df):
    df = df.copy()
    df["reviews.rating"] = pd.to_numeric(df["reviews.rating"], errors="coerce")
    return df[df["reviews.rating"].between(1, 5)]


def deduplicate(df):
    # drop_duplicates treats NaN as equal, which would collapse distinct reviews
    # that share text+rating but both have a missing `name`. Only dedup rows
    # that have a real name; keep all name-less rows untouched.
    named = df[df["name"].notna()]
    unnamed = df[df["name"].isna()]
    named = named.drop_duplicates(subset=["name", "reviews.text", "reviews.rating"])
    return pd.concat([named, unnamed]).sort_index()


def add_sentiment_label(df):
    df = df.copy()
    df["sentiment"] = df["reviews.rating"].round().astype(int).map(RATING_TO_SENTIMENT)
    return df[df["sentiment"].notna()]


def normalize_whitespace(df, columns=("reviews.text", "reviews.title")):
    df = df.copy()
    for col in columns:
        df[col] = df[col].astype(str).str.replace(r"\s+", " ", regex=True).str.strip()
    return df
