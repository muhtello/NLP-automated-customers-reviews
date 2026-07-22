"""Pydantic request/response models for the API."""

from pydantic import BaseModel, Field

from src.models_registry import DEFAULT_MODEL_KEY


class PredictRequest(BaseModel):
    text: str = Field(min_length=1)
    model: str = DEFAULT_MODEL_KEY


class PredictResponse(BaseModel):
    label: str
    confidence: float


class ModelInfo(BaseModel):
    key: str
    display_name: str


class ClassMetrics(BaseModel):
    precision: float
    recall: float
    f1_score: float = Field(alias="f1-score")
    support: float

    model_config = {"populate_by_name": True}


class SentimentMetrics(BaseModel):
    accuracy: float
    negative: ClassMetrics
    positive: ClassMetrics
    macro_avg: ClassMetrics
    confusion_matrix_url: str
