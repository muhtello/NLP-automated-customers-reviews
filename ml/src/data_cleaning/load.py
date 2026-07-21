"""Load and standardize the three raw Datafiniti CSV exports."""

import pandas as pd

RAW_FILES = [
    "1429_1.csv",
    "Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv",
    "Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv",
]

# Columns we keep for the NLP tasks; not every raw file has all of them.
KEEP_COLUMNS = [
    "id",
    "name",
    "brand",
    "categories",
    "primaryCategories",
    "reviews.date",
    "reviews.rating",
    "reviews.text",
    "reviews.title",
    "reviews.doRecommend",
]


def load_raw_file(data_dir, filename):
    path = f"{data_dir}/{filename}"
    df = pd.read_csv(path, usecols=lambda c: c in KEEP_COLUMNS, low_memory=False)
    # Reindex so every file has the same columns, filling absent ones with NaN.
    return df.reindex(columns=KEEP_COLUMNS)


def load_all_raw(data_dir):
    frames = [load_raw_file(data_dir, f) for f in RAW_FILES]
    return pd.concat(frames, ignore_index=True)
