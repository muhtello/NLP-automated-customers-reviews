"""Loads trained sentiment models on demand and runs inference on review text."""

import os
from functools import lru_cache

from transformers import pipeline

from src.models_registry import HF_HUB_REPO_IDS, model_dir


@lru_cache(maxsize=1)
def _get_classifier(model_key: str):
    hub_repo_id = HF_HUB_REPO_IDS.get(model_key)
    if hub_repo_id:
        token = os.environ.get("HF_TOKEN")
        return pipeline("text-classification", model=hub_repo_id, tokenizer=hub_repo_id, token=token)

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
