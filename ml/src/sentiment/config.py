"""Shared constants for the sentiment classification models."""

LABELS = ["Negative", "Positive"]
LABEL2ID = {label: idx for idx, label in enumerate(LABELS)}
ID2LABEL = {idx: label for label, idx in LABEL2ID.items()}

MAX_SEQUENCE_LENGTH = 128
RANDOM_SEED = 42

CLEANED_DATA_PATH = "outputs/cleaned_reviews.parquet"

TRAIN_FRACTION = 0.8
VAL_FRACTION = 0.1
# Remaining fraction (0.1) is used for the held-out test set.

# Every model here is fine-tuned from scratch on the same 2-class (Negative/Positive)
# dataset, so results are directly comparable across architectures. nlptown and cardiffnlp
# are pretrained on different label schemes (5-star, 3-class tweets) - their classification
# heads are replaced (ignore_mismatched_sizes=True) and retrained for this task, same as
# the general-purpose models.
MODEL_REGISTRY: dict[str, dict[str, str]] = {
    "bert": {
        "pretrained_name": "bert-base-uncased",
        "display_name": "BERT (bert-base-uncased)",
    },
    "distilbert": {
        "pretrained_name": "distilbert-base-uncased",
        "display_name": "DistilBERT (distilbert-base-uncased)",
    },
    "roberta": {
        "pretrained_name": "roberta-base",
        "display_name": "RoBERTa (roberta-base)",
    },
    "nlptown-multilingual": {
        "pretrained_name": "nlptown/bert-base-multilingual-uncased-sentiment",
        "display_name": "Multilingual BERT (nlptown)",
    },
    "cardiffnlp-twitter": {
        "pretrained_name": "cardiffnlp/twitter-roberta-base-sentiment",
        "display_name": "Twitter RoBERTa (cardiffnlp)",
    },
}


def model_output_dir(model_key: str) -> str:
    return f"outputs/sentiment_model/{model_key}"


def eval_output_dir(model_key: str) -> str:
    return f"outputs/sentiment_eval/{model_key}"
