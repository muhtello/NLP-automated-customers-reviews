"""Shared constants for the sentiment classification model."""

MODEL_NAME = "bert-base-uncased"

LABELS = ["Negative", "Positive"]
LABEL2ID = {label: idx for idx, label in enumerate(LABELS)}
ID2LABEL = {idx: label for label, idx in LABEL2ID.items()}

MAX_SEQUENCE_LENGTH = 128
RANDOM_SEED = 42

CLEANED_DATA_PATH = "outputs/cleaned_reviews.parquet"
MODEL_OUTPUT_DIR = "outputs/sentiment_model"
EVAL_OUTPUT_DIR = "outputs/sentiment_eval"

TRAIN_FRACTION = 0.8
VAL_FRACTION = 0.1
# Remaining fraction (0.1) is used for the held-out test set.
