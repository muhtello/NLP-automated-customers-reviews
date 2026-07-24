"""Metadata for the sentiment models the API can serve.

Mirrors ml/src/sentiment/config.py's MODEL_REGISTRY keys and display names. Kept as a
small duplicated constant (not an import from ml/) per the project's ml/api boundary:
the two sides share data artifacts, not code.
"""

from pathlib import Path

MODEL_REGISTRY: dict[str, str] = {
    "bert": "BERT (bert-base-uncased)",
    "distilbert": "DistilBERT (distilbert-base-uncased)",
    "roberta": "RoBERTa (roberta-base)",
    "nlptown-multilingual": "Multilingual BERT (nlptown)",
    "cardiffnlp-twitter": "Twitter RoBERTa (cardiffnlp)",
}

DEFAULT_MODEL_KEY = "bert"

# Models served from a private Hugging Face Hub repo instead of a local
# ml/outputs/ checkout (requires HF_TOKEN in api/.env for private repos).
HF_HUB_REPO_IDS: dict[str, str] = {
    "cardiffnlp-twitter": "holder212/Consumer_Reviews_of_Amazon_Products_May19",
}

_ML_OUTPUTS_DIR = Path(__file__).resolve().parents[2] / "ml" / "outputs"
SENTIMENT_EVAL_ROOT = _ML_OUTPUTS_DIR / "sentiment_eval"


def model_dir(model_key: str) -> Path:
    return _ML_OUTPUTS_DIR / "sentiment_model" / model_key


def eval_dir(model_key: str) -> Path:
    return _ML_OUTPUTS_DIR / "sentiment_eval" / model_key


def available_model_keys() -> list[str]:
    """Model keys with an eval report on disk, and weights either on Hugging Face Hub or on disk."""
    return [
        key
        for key in MODEL_REGISTRY
        if (eval_dir(key) / "classification_report.json").exists()
        and (key in HF_HUB_REPO_IDS or (model_dir(key) / "config.json").exists())
    ]
