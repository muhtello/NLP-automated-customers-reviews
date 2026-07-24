"""Train and evaluate every model in MODEL_REGISTRY that isn't already trained.

Usage:
    python -m src.sentiment.train_all
Run from the `ml/` directory.
"""

import os

from src.sentiment.config import MODEL_REGISTRY, eval_output_dir, model_output_dir
from src.sentiment.evaluate import main as evaluate_model
from src.sentiment.train import main as train_model


def main() -> None:
    for model_key in MODEL_REGISTRY:
        trained = os.path.exists(f"{model_output_dir(model_key)}/config.json")
        evaluated = os.path.exists(f"{eval_output_dir(model_key)}/classification_report.json")
        if trained and evaluated:
            print(f"[{model_key}] Already trained and evaluated, skipping.")
            continue
        if not trained:
            print(f"[{model_key}] Training...")
            train_model(model_key)
        print(f"[{model_key}] Evaluating...")
        evaluate_model(model_key)


if __name__ == "__main__":
    main()
