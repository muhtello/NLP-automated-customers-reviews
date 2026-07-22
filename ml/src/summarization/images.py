"""Product image URL lookup, built directly from the raw Datafiniti exports.

Only two of the three raw CSVs carry an `imageURLs` column, and that column
never survives into `reviews_with_meta_categories.csv` (the clustering
pipeline's output, built on another branch). Reading it straight from the raw
files here avoids depending on that pipeline's schema.
"""

import pandas as pd

RAW_FILES_WITH_IMAGES = [
    "Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv",
    "Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv",
]


def build_image_lookup(data_dir: str) -> dict[str, str]:
    """Map cleaned product name -> first image URL, first file/row wins."""
    lookup: dict[str, str] = {}
    for filename in RAW_FILES_WITH_IMAGES:
        df = pd.read_csv(f"{data_dir}/{filename}", usecols=["name", "imageURLs"])
        df = df.dropna(subset=["imageURLs"])
        df["name"] = df["name"].astype(str).str.split(",").str[0].str.strip()
        for name, urls in zip(df["name"], df["imageURLs"]):
            if name not in lookup:
                lookup[name] = urls.split(",")[0].strip()
    return lookup
