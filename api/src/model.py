"""Loads trained sentiment models on demand and runs inference on review text."""

from functools import lru_cache

from transformers import pipeline

from src.models_registry import MODEL_REGISTRY, model_dir


@lru_cache(maxsize=len(MODEL_REGISTRY))
def _get_classifier(model_key: str):
    path = str(model_dir(model_key))
    return pipeline("text-classification", model=path, tokenizer=path)


def predict_sentiment(text: str, model_key: str) -> dict:
    result = _get_classifier(model_key)(text, truncation=True)[0]
    return {"label": result["label"], "confidence": result["score"]}


def predict_sentiment_batch(texts: list[str], model_key: str) -> list[dict]:
    if not texts:
        return []
    results = _get_classifier(model_key)(texts, truncation=True, batch_size=16)
    return [{"label": result["label"], "confidence": result["score"]} for result in results]
