"""FastAPI application entry point.

Usage:
    uvicorn src.main:app --reload
Run from the `api/` directory.
"""

from fastapi import FastAPI

app = FastAPI(title="Customer Reviews API")


@app.get("/health")
def health_check() -> dict[str, str]:
    """Report service liveness for uptime checks and deploy probes."""
    return {"status": "ok"}
