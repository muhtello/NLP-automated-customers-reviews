"""Shopping-assistant chat engine.

Wraps the OpenAI chat API with per-category context pulled from the same
precomputed summary artifacts the /categories endpoints serve (see
src/summaries_registry.py) — no separate data store for the chatbot.
"""

import os

from openai import OpenAI

from src.schemas import ChatMessage
from src.summaries_registry import load_summary

CHAT_MODEL = "gpt-4o-mini"


class ChatEngine:
    def __init__(self) -> None:
        self._client: OpenAI | None = None

    def _client_or_raise(self) -> OpenAI:
        if self._client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise RuntimeError("OPENAI_API_KEY is not set.")
            self._client = OpenAI(api_key=api_key)
        return self._client

    def reply(self, message: str, category_slug: str | None, history: list[ChatMessage]) -> str:
        summary = load_summary(category_slug) if category_slug else None

        if summary is not None:
            category_name = summary["stats"]["category"]
            system_prompt = (
                f"You are a helpful shopping assistant for the {category_name} category. "
                f"Recommend products and answer questions using this context:\n{summary['article']}"
            )
        else:
            system_prompt = (
                "You are a helpful shopping assistant for an Amazon product review dashboard. "
                "No specific category is selected, so answer generally and suggest the user "
                "browse a category page for more detailed recommendations."
            )

        messages = [{"role": "system", "content": system_prompt}]
        messages += [{"role": entry.role, "content": entry.content} for entry in history]
        messages.append({"role": "user", "content": message})

        response = self._client_or_raise().chat.completions.create(model=CHAT_MODEL, messages=messages)
        return response.choices[0].message.content
