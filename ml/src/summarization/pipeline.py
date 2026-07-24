"""Precompute one recommendation article per meta_category.

Usage:
    python -m src.summarization.pipeline
Run from the `ml/` directory (so the `data/` and `outputs/` paths resolve).
"""

import json
import os
import re

import pandas as pd

from . import config
from .aggregate import build_category_stats
from .generate import generate_summary
from .prompt import build_prompt


def _slugify(category_name: str) -> str:
    slug = category_name.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def run() -> None:
    os.makedirs(config.SUMMARY_OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(config.META_CATEGORY_DATA_PATH)
    print(f"Loaded {len(df)} rows, {df['meta_category'].nunique()} meta categories")

    for category_name, category_df in df.groupby("meta_category"):
        print(f"=== {category_name} ({len(category_df)} reviews) ===")

        stats = build_category_stats(category_df, category_name)
        prompt = build_prompt(stats)
        article = generate_summary(prompt)

        output = {"stats": stats, "article": article}
        slug = _slugify(category_name)
        output_path = os.path.join(config.SUMMARY_OUTPUT_DIR, f"{slug}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(f"Saved {output_path}")


if __name__ == "__main__":
    run()
