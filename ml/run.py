"""Run the full ML pipeline: clean data -> train sentiment model -> evaluate.

Usage (from the `ml/` directory, with venv active):
    venv\\Scripts\\python.exe run.py
    venv\\Scripts\\python.exe run.py --skip-clean
    venv\\Scripts\\python.exe run.py --skip-clean --skip-train
"""

import argparse

from src.data_cleaning.pipeline import run as run_cleaning
from src.sentiment.train import main as run_training
from src.sentiment.evaluate import main as run_evaluation


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-clean", action="store_true", help="Skip data cleaning (reuse outputs/cleaned_reviews.parquet)")
    parser.add_argument("--skip-train", action="store_true", help="Skip training (reuse outputs/sentiment_model)")
    args = parser.parse_args()

    if not args.skip_clean:
        print("=== Step 1/3: cleaning data ===")
        run_cleaning()
    else:
        print("=== Step 1/3: skipped ===")

    if not args.skip_train:
        print("=== Step 2/3: training sentiment model ===")
        run_training()
    else:
        print("=== Step 2/3: skipped ===")

    print("=== Step 3/3: evaluating sentiment model ===")
    run_evaluation()


if __name__ == "__main__":
    main()
