"""Loads the trained sentiment model and runs inference on review text."""

from pathlib import Path

from transformers import pipeline

MODEL_DIR = Path(__file__).resolve().parents[2] / "ml" / "outputs" / "sentiment_model"

_classifier = pipeline("text-classification", model=str(MODEL_DIR), tokenizer=str(MODEL_DIR))


def predict_sentiment(text: str) -> dict:
    result = _classifier(text, truncation=True)[0]
    return {"label": result["label"], "confidence": result["score"]}
