"""Run the review summarization pipeline (Objective 3).

Usage (from the `ml/` directory, with venv active):
    venv\\Scripts\\python.exe run_summarization.py

Requires OPENAI_API_KEY to be set in ml/.env - see src/summarization/config.py.
"""

from src.summarization.pipeline import run

if __name__ == "__main__":
    run()
