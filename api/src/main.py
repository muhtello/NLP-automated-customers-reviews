"""FastAPI application entry point.

Usage:
    uvicorn src.main:app --reload
Run from the `api/` directory.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.metrics import get_sentiment_metrics
from src.model import predict_sentiment
from src.models_registry import MODEL_REGISTRY, SENTIMENT_EVAL_ROOT, available_model_keys
from src.schemas import (
    CategoryListItem,
    CategorySummary,
    ModelInfo,
    PredictRequest,
    PredictResponse,
    SentimentMetrics,
)
from src.summaries_registry import available_slugs, load_summary

app = FastAPI(title="Customer Reviews API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static/sentiment_eval", StaticFiles(directory=str(SENTIMENT_EVAL_ROOT)), name="sentiment_eval")


def _require_available(model_key: str) -> None:
    if model_key not in available_model_keys():
        raise HTTPException(status_code=404, detail=f"Model '{model_key}' is not trained/available yet.")


@app.get("/health")
def health_check() -> dict[str, str]:
    """Report service liveness for uptime checks and deploy probes."""
    return {"status": "ok"}


@app.get("/models", response_model=list[ModelInfo])
def list_models() -> list[ModelInfo]:
    return [ModelInfo(key=key, display_name=MODEL_REGISTRY[key]) for key in available_model_keys()]


@app.get("/metrics/sentiment", response_model=SentimentMetrics)
def sentiment_metrics(model: str = "bert") -> SentimentMetrics:
    _require_available(model)
    return SentimentMetrics(**get_sentiment_metrics(model))


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    _require_available(request.model)
    return PredictResponse(**predict_sentiment(request.text, request.model))


@app.get("/categories", response_model=list[CategoryListItem])
def list_categories() -> list[CategoryListItem]:
    items = []
    for slug in available_slugs():
        summary = load_summary(slug)
        if summary is not None:
            stats = summary["stats"]
            items.append(
                CategoryListItem(
                    slug=slug,
                    category=stats["category"],
                    total_reviews=stats["total_reviews"],
                    avg_rating=stats["avg_rating"],
                    pct_negative=stats["pct_negative"],
                )
            )
    return items


@app.get("/categories/{slug}", response_model=CategorySummary)
def get_category(slug: str) -> CategorySummary:
    summary = load_summary(slug)
    if summary is None:
        raise HTTPException(status_code=404, detail=f"Category '{slug}' not found.")
    return CategorySummary(slug=slug, **summary)
