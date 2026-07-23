"""FastAPI application entry point.

Usage:
    uvicorn src.main:app --reload
Run from the `api/` directory.
"""

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

load_dotenv()

from src.chatbot_engine import ChatEngine
from src.metrics import get_sentiment_metrics
from src.model import predict_sentiment, predict_sentiment_batch
from src.models_registry import MODEL_REGISTRY, SENTIMENT_EVAL_ROOT, available_model_keys
from src.products import get_product_reviews, search_products
from src.schemas import (
    CategoryListItem,
    CategorySummary,
    ChatRequest,
    ChatResponse,
    ModelInfo,
    PredictRequest,
    PredictResponse,
    ProductAnalysis,
    ProductAnalyzeRequest,
    ProductListItem,
    SentimentMetrics,
)
from src.summaries_registry import available_slugs, load_summary

app = FastAPI(title="Customer Reviews API")
chat_engine = ChatEngine()

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


@app.get("/products", response_model=list[ProductListItem])
def list_products(q: str = "") -> list[ProductListItem]:
    return [ProductListItem(**item) for item in search_products(q)]


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    if request.category_slug is not None and request.category_slug not in available_slugs():
        raise HTTPException(status_code=404, detail=f"Category '{request.category_slug}' not found.")
    try:
        reply = chat_engine.reply(request.message, request.category_slug, request.history)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    return ChatResponse(reply=reply)


@app.post("/products/analyze", response_model=ProductAnalysis)
def analyze_product(request: ProductAnalyzeRequest) -> ProductAnalysis:
    _require_available(request.model)
    reviews, total, avg_rating = get_product_reviews(request.name)
    if total == 0:
        raise HTTPException(status_code=404, detail=f"Product '{request.name}' has no reviews on file.")

    predictions = predict_sentiment_batch(reviews, request.model)
    positive_count = sum(1 for p in predictions if p["label"] == "Positive")
    negative_count = len(predictions) - positive_count
    sample_size = len(predictions)

    return ProductAnalysis(
        name=request.name,
        model=request.model,
        review_count=total,
        sample_size=sample_size,
        avg_rating=avg_rating,
        positive_count=positive_count,
        negative_count=negative_count,
        pct_positive=positive_count / sample_size if sample_size else 0.0,
        pct_negative=negative_count / sample_size if sample_size else 0.0,
    )
