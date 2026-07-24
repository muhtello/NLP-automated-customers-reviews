"""Reads the precomputed sentiment model evaluation reports produced by ml/."""

import json

from src.models_registry import eval_dir


def get_sentiment_metrics(model_key: str) -> dict:
    report = json.loads((eval_dir(model_key) / "classification_report.json").read_text())
    return {
        "accuracy": report["accuracy"],
        "negative": report["Negative"],
        "positive": report["Positive"],
        "macro_avg": report["macro avg"],
        "confusion_matrix_url": f"/static/sentiment_eval/{model_key}/confusion_matrix.png",
    }
