"""Evaluate a fine-tuned sentiment model on the held-out test split.

Usage:
    python -m src.sentiment.evaluate --model bert
Run from the `ml/` directory, after `python -m src.sentiment.train --model bert`.
"""

import argparse
import json
import os

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, confusion_matrix
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer

from src.sentiment.config import CLEANED_DATA_PATH, LABELS, MODEL_REGISTRY, eval_output_dir, model_output_dir
from src.sentiment.dataset import build_dataset_dict, load_cleaned_reviews, split_dataset, tokenize_dataset_dict


def main(model_key: str) -> None:
    output_dir = model_output_dir(model_key)
    eval_dir = eval_output_dir(model_key)
    os.makedirs(eval_dir, exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(output_dir)
    model = AutoModelForSequenceClassification.from_pretrained(output_dir)

    df = load_cleaned_reviews(CLEANED_DATA_PATH)
    _, _, test_df = split_dataset(df)
    dataset_dict = build_dataset_dict(test_df, test_df, test_df)
    tokenized_test = tokenize_dataset_dict(dataset_dict, tokenizer)["test"]

    predictions = Trainer(model=model).predict(tokenized_test)  # type: ignore
    predicted_labels = np.argmax(predictions.predictions, axis=1)
    true_labels = predictions.label_ids
    assert true_labels is not None

    report = classification_report(true_labels, predicted_labels, target_names=LABELS, output_dict=True)
    print(f"[{model_key}]")
    print(classification_report(true_labels, predicted_labels, target_names=LABELS))

    with open(f"{eval_dir}/classification_report.json", "w") as f:
        json.dump(report, f, indent=2)

    matrix = confusion_matrix(true_labels, predicted_labels)
    ConfusionMatrixDisplay(confusion_matrix=matrix, display_labels=LABELS).plot(cmap="Blues")
    plt.title(f"{MODEL_REGISTRY[model_key]['display_name']} - Confusion Matrix (Test Set)")
    plt.tight_layout()
    plt.savefig(f"{eval_dir}/confusion_matrix.png")
    plt.close()
    print(f"[{model_key}] Saved report and confusion matrix to {eval_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, choices=list(MODEL_REGISTRY))
    args = parser.parse_args()
    main(args.model)
