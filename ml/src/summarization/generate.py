"""Thin OpenAI client wrapper for generating one summary article from a prompt."""

import time

from openai import APIError, OpenAI, RateLimitError

from . import config

_MAX_ATTEMPTS = 3
_BACKOFF_SECONDS = 5


def generate_summary(prompt: str) -> str:
    """Call the chat completions API and return the generated article text.

    Retries a few times on rate-limit / transient API errors with a fixed backoff -
    this pipeline only makes ~4-6 calls total, so anything fancier is unnecessary.
    """
    if not config.OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Add it to ml/.env (OPENAI_API_KEY=sk-...) "
            "before running the summarization pipeline."
        )

    client = OpenAI(api_key=config.OPENAI_API_KEY)

    last_error: Exception | None = None
    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            response = client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except (RateLimitError, APIError) as error:
            last_error = error
            if attempt < _MAX_ATTEMPTS:
                time.sleep(_BACKOFF_SECONDS * attempt)

    raise RuntimeError(f"OpenAI request failed after {_MAX_ATTEMPTS} attempts: {last_error}")
