"""Evaluate the fine-tuned sentiment model on the held-out test split.

Usage:
    python -m src.sentiment.evaluate
Run from the `ml/` directory, after `python -m src.sentiment.train`.
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, confusion_matrix
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer

from src.sentiment.config import CLEANED_DATA_PATH, EVAL_OUTPUT_DIR, LABELS, MODEL_OUTPUT_DIR
from src.sentiment.dataset import build_dataset_dict, load_cleaned_reviews, split_dataset, tokenize_dataset_dict


def main() -> None:
    os.makedirs(EVAL_OUTPUT_DIR, exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_OUTPUT_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_OUTPUT_DIR)

    df = load_cleaned_reviews(CLEANED_DATA_PATH)
    _, _, test_df = split_dataset(df)
    dataset_dict = build_dataset_dict(test_df, test_df, test_df)
    tokenized_test = tokenize_dataset_dict(dataset_dict, tokenizer)["test"]

    predictions = Trainer(model=model).predict(tokenized_test)  # type: ignore
    predicted_labels = np.argmax(predictions.predictions, axis=1)
    true_labels = predictions.label_ids
    assert true_labels is not None

    report = classification_report(true_labels, predicted_labels, target_names=LABELS, output_dict=True)
    print(classification_report(true_labels, predicted_labels, target_names=LABELS))

    with open(f"{EVAL_OUTPUT_DIR}/classification_report.json", "w") as f:
        json.dump(report, f, indent=2)

    matrix = confusion_matrix(true_labels, predicted_labels)
    ConfusionMatrixDisplay(confusion_matrix=matrix, display_labels=LABELS).plot(cmap="Blues")
    plt.title("Sentiment Classification - Confusion Matrix (Test Set)")
    plt.tight_layout()
    plt.savefig(f"{EVAL_OUTPUT_DIR}/confusion_matrix.png")
    print(f"Saved report and confusion matrix to {EVAL_OUTPUT_DIR}")


if __name__ == "__main__":
    main()
