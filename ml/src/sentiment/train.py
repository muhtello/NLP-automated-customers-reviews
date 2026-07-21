"""Fine-tune bert-base-uncased for 3-class review sentiment.

Usage:
    python -m src.sentiment.train
Run from the `ml/` directory.
"""

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
    MODEL_NAME,
    MODEL_OUTPUT_DIR,
    RANDOM_SEED,
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


def main() -> None:
    df = load_cleaned_reviews(CLEANED_DATA_PATH)
    train_df, val_df, test_df = split_dataset(df)
    print(f"Split sizes -> train: {len(train_df)}, val: {len(val_df)}, test: {len(test_df)}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    dataset_dict = build_dataset_dict(train_df, val_df, test_df)
    tokenized = tokenize_dataset_dict(dataset_dict, tokenizer)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(LABELS),
        id2label=ID2LABEL,
        label2id=LABEL2ID,
    )
    class_weights = compute_class_weights(train_df["label"].tolist())

    training_args = TrainingArguments(
        output_dir=f"{MODEL_OUTPUT_DIR}/checkpoints",
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
    print("Test metrics:", test_metrics)

    trainer.save_model(MODEL_OUTPUT_DIR)
    tokenizer.save_pretrained(MODEL_OUTPUT_DIR)
    print(f"Model saved to {MODEL_OUTPUT_DIR}")


if __name__ == "__main__":
    main()
