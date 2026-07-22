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

_ML_OUTPUTS_DIR = Path(__file__).resolve().parents[2] / "ml" / "outputs"
SENTIMENT_EVAL_ROOT = _ML_OUTPUTS_DIR / "sentiment_eval"


def model_dir(model_key: str) -> Path:
    return _ML_OUTPUTS_DIR / "sentiment_model" / model_key


def eval_dir(model_key: str) -> Path:
    return _ML_OUTPUTS_DIR / "sentiment_eval" / model_key


def available_model_keys() -> list[str]:
    """Model keys that have both a trained model directory and an eval report on disk."""
    return [
        key
        for key in MODEL_REGISTRY
        if (model_dir(key) / "config.json").exists() and (eval_dir(key) / "classification_report.json").exists()
    ]
