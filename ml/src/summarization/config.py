"""Shared constants for the review summarization pipeline (Objective 3)."""

import os

# Load ml/.env (e.g. OPENAI_API_KEY) so it's set before the openai client is
# constructed, without adding a python-dotenv dependency. Mirrors
# src/sentiment/config.py's approach for consistency.
_ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
if os.path.exists(_ENV_PATH):
    with open(_ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"

# Paths are relative to the `ml/` directory, matching data_cleaning/pipeline.py
# (DATA_DIR = "../data") and sentiment/config.py (CLEANED_DATA_PATH = "outputs/...").
META_CATEGORY_DATA_PATH = "../data/reviews_with_meta_categories.csv"
SUMMARY_OUTPUT_DIR = "outputs/summaries"

# Products with fewer reviews than this are excluded from top/worst ranking so a
# single 5-star or 1-star review can't dominate the picks for a category.
MIN_REVIEWS_PER_PRODUCT = 5
TOP_N_PRODUCTS = 3
MAX_COMPLAINT_SAMPLES = 8
RANDOM_SEED = 42
