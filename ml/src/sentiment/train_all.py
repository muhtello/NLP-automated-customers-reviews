"""Train and evaluate every model in MODEL_REGISTRY that isn't already trained.

Usage:
    python -m src.sentiment.train_all
Run from the `ml/` directory.
"""

import os

from src.sentiment.config import MODEL_REGISTRY, model_output_dir
from src.sentiment.evaluate import main as evaluate_model
from src.sentiment.train import main as train_model


def main() -> None:
    for model_key in MODEL_REGISTRY:
        if os.path.exists(f"{model_output_dir(model_key)}/config.json"):
            print(f"[{model_key}] Already trained, skipping.")
            continue
        print(f"[{model_key}] Training...")
        train_model(model_key)
        print(f"[{model_key}] Evaluating...")
        evaluate_model(model_key)


if __name__ == "__main__":
    main()
