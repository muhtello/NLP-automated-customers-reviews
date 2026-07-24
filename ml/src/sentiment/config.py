"""Shared constants for the sentiment classification models."""

import os

# Load ml/.env (e.g. HF_TOKEN) so it's set before any huggingface_hub/transformers
# calls happen, without adding a python-dotenv dependency.
_ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
if os.path.exists(_ENV_PATH):
    with open(_ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())

LABELS = ["Negative", "Positive"]
LABEL2ID = {label: idx for idx, label in enumerate(LABELS)}
ID2LABEL = {idx: label for label, idx in LABEL2ID.items()}

MAX_SEQUENCE_LENGTH = 128
RANDOM_SEED = 42

CLEANED_DATA_PATH = "outputs/cleaned_reviews.parquet"

TRAIN_FRACTION = 0.8
VAL_FRACTION = 0.1
# Remaining fraction (0.1) is used for the held-out test set.

# Every model here is fine-tuned from scratch on the same 2-class (Negative/Positive)
# dataset, so results are directly comparable across architectures. nlptown and cardiffnlp
# are pretrained on different label schemes (5-star, 3-class tweets) - their classification
# heads are replaced (ignore_mismatched_sizes=True) and retrained for this task, same as
# the general-purpose models.
MODEL_REGISTRY: dict[str, dict[str, str]] = {
    "bert": {
        "pretrained_name": "bert-base-uncased",
        "display_name": "BERT (bert-base-uncased)",
        "description": "A strong general-purpose model for sentiment analysis."
    },
    "distilbert": {
        "pretrained_name": "distilbert-base-uncased",
        "display_name": "DistilBERT (distilbert-base-uncased)",
        "description": "Lightweight and fast, ideal for limited resources."
    },
    "roberta": {
        "pretrained_name": "roberta-base",
        "display_name": "RoBERTa (roberta-base)",
        "description": "More robust to nuanced sentiment variations"
    },
    "nlptown-multilingual": {
        "pretrained_name": "nlptown/bert-base-multilingual-uncased-sentiment",
        "display_name": "Multilingual BERT (nlptown)",
        "description": "Handles multiple languages, useful for diverse datasets."
    },
    "cardiffnlp-twitter": {
        "pretrained_name": "cardiffnlp/twitter-roberta-base-sentiment",
        "display_name": "Twitter RoBERTa (cardiffnlp)",
        "description": "Optimized for short texts like social media reviews"
    },
}


def model_output_dir(model_key: str) -> str:
    return f"outputs/sentiment_model/{model_key}"


def eval_output_dir(model_key: str) -> str:
    return f"outputs/sentiment_eval/{model_key}"
