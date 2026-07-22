"""Fine-tune a transformer for 2-class (Negative/Positive) review sentiment.

Usage:
    python -m src.sentiment.train --model bert
Run from the `ml/` directory. `--model` must be a key in MODEL_REGISTRY (config.py).
"""

import argparse

import numpy as np
import torch
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.utils.class_weight import compute_class_weight
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    EvalPrediction,
    Trainer,
    TrainingArguments,
)

from src.sentiment.config import (
    CLEANED_DATA_PATH,
    ID2LABEL,
    LABEL2ID,
    LABELS,
    MODEL_REGISTRY,
    RANDOM_SEED,
    model_output_dir,
)
from src.sentiment.dataset import (
    build_dataset_dict,
    load_cleaned_reviews,
    split_dataset,
    tokenize_dataset_dict,
)


def compute_class_weights(train_labels: list[int]) -> torch.Tensor:
    """Inverse-frequency class weights to counter the Positive-heavy imbalance."""
    weights = compute_class_weight(
        class_weight="balanced",
        classes=np.arange(len(LABELS)),
        y=np.array(train_labels),
    )
    return torch.tensor(weights, dtype=torch.float32)


class WeightedTrainer(Trainer):
    """Trainer variant that applies class weights to the cross-entropy loss."""

    def __init__(self, class_weights: torch.Tensor, **kwargs):
        super().__init__(**kwargs)
        self.class_weights = class_weights

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits
        loss_fn = torch.nn.CrossEntropyLoss(weight=self.class_weights.to(logits.device))
        loss = loss_fn(logits, labels)
        return (loss, outputs) if return_outputs else loss


def compute_metrics(eval_pred: EvalPrediction) -> dict:
    """Compute accuracy plus macro precision/recall/F1 for the eval loop."""
    predictions = np.argmax(eval_pred.predictions, axis=1)
    labels = eval_pred.label_ids
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average="macro", zero_division=0)
    return {
        "accuracy": accuracy_score(labels, predictions),
        "precision_macro": precision,
        "recall_macro": recall,
        "f1_macro": f1,
    }


def main(model_key: str) -> None:
    pretrained_name = MODEL_REGISTRY[model_key]["pretrained_name"]
    output_dir = model_output_dir(model_key)

    device_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
    print(f"[{model_key}] CUDA available: {torch.cuda.is_available()} -> training on {device_name}")

    df = load_cleaned_reviews(CLEANED_DATA_PATH)
    train_df, val_df, test_df = split_dataset(df)
    print(f"[{model_key}] Split sizes -> train: {len(train_df)}, val: {len(val_df)}, test: {len(test_df)}")

    tokenizer = AutoTokenizer.from_pretrained(pretrained_name)
    dataset_dict = build_dataset_dict(train_df, val_df, test_df)
    tokenized = tokenize_dataset_dict(dataset_dict, tokenizer)

    model = AutoModelForSequenceClassification.from_pretrained(
        pretrained_name,
        num_labels=len(LABELS),
        id2label=ID2LABEL,
        label2id=LABEL2ID,
        ignore_mismatched_sizes=True,
    )
    class_weights = compute_class_weights(train_df["label"].tolist())

    training_args = TrainingArguments(
        output_dir=f"{output_dir}/checkpoints",
        num_train_epochs=2,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        learning_rate=2e-5,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1_macro",
        logging_steps=50,
        seed=RANDOM_SEED,
        report_to=[],
    )

    trainer = WeightedTrainer(
        class_weights=class_weights,
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["validation"],
        processing_class=tokenizer,
        compute_metrics=compute_metrics,
    )

    trainer.train()

    test_metrics = trainer.evaluate(tokenized["test"], metric_key_prefix="test")
    print(f"[{model_key}] Test metrics:", test_metrics)

    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    # Persist the exact test split used for this run so evaluate.py doesn't have
    # to re-derive it (which would silently diverge if the cleaned dataset is
    # ever regenerated with a different row order).
    test_df.to_parquet(f"{output_dir}/test_split.parquet", index=False)
    print(f"[{model_key}] Model saved to {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, choices=list(MODEL_REGISTRY))
    args = parser.parse_args()
    main(args.model)
