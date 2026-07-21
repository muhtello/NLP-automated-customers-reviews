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
