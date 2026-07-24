"""Smoke tests for the FastAPI app."""

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health_check() -> None:
    """The health endpoint should report ok with a 200 status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict() -> None:
    """The predict endpoint should return a known label and a valid confidence."""
    response = client.post("/predict", json={"text": "This product is amazing, I love it!"})
    assert response.status_code == 200
    body = response.json()
    assert body["label"] in {"Negative", "Positive"}
    assert 0 <= body["confidence"] <= 1


def test_sentiment_metrics() -> None:
    """The metrics endpoint should return the precomputed held-out test report for the bert model."""
    response = client.get("/metrics/sentiment", params={"model": "bert"})
    assert response.status_code == 200
    body = response.json()
    assert 0 <= body["accuracy"] <= 1
    assert body["negative"]["support"] > 0
    assert body["confusion_matrix_url"] == "/static/sentiment_eval/bert/confusion_matrix.png"


def test_list_models() -> None:
    """The models endpoint should include at least the bert model, which is always trained."""
    response = client.get("/models")
    assert response.status_code == 200
    keys = [model["key"] for model in response.json()]
    assert "bert" in keys


def test_predict_unknown_model() -> None:
    """Requesting an untrained/unknown model should return 404, not a crash."""
    response = client.post("/predict", json={"text": "Great product", "model": "not-a-real-model"})
    assert response.status_code == 404
