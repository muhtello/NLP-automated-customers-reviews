"""Push the trained sentiment model to a private Hugging Face Hub repo.

Usage (from the `ml/` directory, with venv active):
    venv\\Scripts\\python.exe run_push_to_hub.py

Edit DEFAULT_MODEL_KEY / DEFAULT_REPO_ID in src/sentiment/push_to_hub.py to
change what gets uploaded and where.

Requires HF_TOKEN to be set in ml/.env - see src/sentiment/push_to_hub.py.
"""

from src.sentiment.push_to_hub import DEFAULT_MODEL_KEY, DEFAULT_REPO_ID, push_model

if __name__ == "__main__":
    push_model(DEFAULT_MODEL_KEY, DEFAULT_REPO_ID)
