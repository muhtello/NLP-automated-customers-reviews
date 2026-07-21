"""FastAPI application entry point.

Usage:
    uvicorn src.main:app --reload
Run from the `api/` directory.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.model import predict_sentiment
from src.schemas import PredictRequest, PredictResponse

app = FastAPI(title="Customer Reviews API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Report service liveness for uptime checks and deploy probes."""
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    return PredictResponse(**predict_sentiment(request.text))
