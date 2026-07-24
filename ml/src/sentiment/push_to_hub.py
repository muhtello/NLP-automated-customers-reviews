"""Push a trained sentiment model to a private Hugging Face Hub repo.

Requires HF_TOKEN in ml/.env (a token with write access, from
https://huggingface.co/settings/tokens).
"""

import argparse
import os

from huggingface_hub import HfApi, login, upload_folder

from src.sentiment.config import model_output_dir

DEFAULT_MODEL_KEY = "cardiffnlp-twitter"
DEFAULT_REPO_ID = "holder212/Consumer_Reviews_of_Amazon_Products_May19"

# Excludes checkpoints/ (training checkpoints, several GB), test_split.parquet
# (eval artifact), and training_args.bin - none are needed to reload the
# model + tokenizer for inference.
IGNORE_PATTERNS = ["checkpoints/*", "checkpoints", "test_split.parquet", "training_args.bin"]


def push_model(model_key: str, repo_id: str) -> None:
    login(token=os.environ["HF_TOKEN"])

    api = HfApi()
    api.create_repo(repo_id, repo_type="model", private=True, exist_ok=True)

    upload_folder(
        folder_path=model_output_dir(model_key),
        repo_id=repo_id,
        repo_type="model",
        ignore_patterns=IGNORE_PATTERNS,
    )

    print(f"Done: https://huggingface.co/{repo_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-key", default="cardiffnlp-twitter")
    parser.add_argument("--repo-id", required=True, help="e.g. your-username/amazon-review-sentiment")
    args = parser.parse_args()

    push_model(args.model_key, args.repo_id)
