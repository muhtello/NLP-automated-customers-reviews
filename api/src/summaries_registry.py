"""Loads precomputed category summary artifacts produced by ml/src/summarization/pipeline.py.

Summaries are static JSON files on disk (ml/outputs/summaries/<slug>.json) — this module
just discovers and reads them, it does not call OpenAI or pandas.
"""

import json
from pathlib import Path

_ML_OUTPUTS_DIR = Path(__file__).resolve().parents[2] / "ml" / "outputs"
SUMMARIES_ROOT = _ML_OUTPUTS_DIR / "summaries"


def available_slugs() -> list[str]:
    if not SUMMARIES_ROOT.exists():
        return []
    return sorted(path.stem for path in SUMMARIES_ROOT.glob("*.json"))


def load_summary(slug: str) -> dict | None:
    path = SUMMARIES_ROOT / f"{slug}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))
