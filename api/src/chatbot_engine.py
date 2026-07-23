"""Shopping-assistant chat engine.

Wraps the OpenAI chat API with per-category context pulled from the same
precomputed summary artifacts the /categories endpoints serve (see
src/summaries_registry.py), plus live product lookups via src/chat_tools.py
(function-calling) so the assistant can answer "does X exist", "compare X's
best/worst review", and "top/worst N products" with real data instead of
just the static category article.
"""

import os

from openai import OpenAI

from src.chat_tools import TOOLS, run_tool
from src.schemas import ChatMessage
from src.summaries_registry import load_summary

CHAT_MODEL = "gpt-4o-mini"

# Once the visible history reaches this many messages, older turns are condensed into one
# summary line before being sent to OpenAI, so context stays bounded on long conversations.
SUMMARY_TRIGGER_LENGTH = 10
KEEP_RECENT_MESSAGES = 4

PERSONA_PROMPTS = {
    "recommender": (
        "You are an enthusiastic, encouraging shopping assistant. Recommend products confidently "
        "and highlight what reviewers loved."
    ),
    "anti_recommender": (
        "You are a sarcastic anti-shopping assistant. Your job is to talk the user out of buying things "
        "by emphasizing complaints, flaws, and buyer's remorse found in the reviews."
    ),
}


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

    def _build_system_prompt(self, category_slug: str | None, mode: str) -> str:
        persona = PERSONA_PROMPTS.get(mode, PERSONA_PROMPTS["recommender"])
        summary = load_summary(category_slug) if category_slug else None

        if summary is not None:
            category_name = summary["stats"]["category"]
            context = (
                f" You're focused on the {category_name} category. Use this background when relevant:\n"
                f"{summary['article']}"
            )
        else:
            context = " No specific category is selected, so answer generally."

        tool_guidance = (
            " You have tools to check whether a product exists, compare its best and worst review, "
            "and rank the best/worst products. Call them whenever the user names a product or asks "
            "for a ranked list, instead of guessing. If a tool reports the product or category was not "
            "found, say plainly that you don't have related products for that — never substitute a "
            "different product/category or invent data to fill the gap."
        )
        return persona + context + tool_guidance

    def _condensed_history(self, client: OpenAI, history: list[ChatMessage]) -> list[dict]:
        if len(history) < SUMMARY_TRIGGER_LENGTH:
            return [{"role": entry.role, "content": entry.content} for entry in history]

        older, recent = history[:-KEEP_RECENT_MESSAGES], history[-KEEP_RECENT_MESSAGES:]
        transcript = "\n".join(f"{entry.role}: {entry.content}" for entry in older)
        summary_prompt = (
            "Summarize this conversation between a user and a shopping assistant in 3-4 sentences, "
            f"keeping any product names, preferences, or conclusions mentioned:\n\n{transcript}"
        )
        summary_response = client.chat.completions.create(
            model=CHAT_MODEL, messages=[{"role": "user", "content": summary_prompt}]
        )
        summary_text = summary_response.choices[0].message.content

        condensed = [{"role": "system", "content": f"Earlier conversation summary: {summary_text}"}]
        condensed += [{"role": entry.role, "content": entry.content} for entry in recent]
        return condensed

    def reply(
        self, message: str, category_slug: str | None, history: list[ChatMessage], mode: str = "recommender"
    ) -> dict:
        client = self._client_or_raise()
        system_prompt = self._build_system_prompt(category_slug, mode)

        messages = [{"role": "system", "content": system_prompt}]
        messages += self._condensed_history(client, history)
        messages.append({"role": "user", "content": message})

        response = client.chat.completions.create(model=CHAT_MODEL, messages=messages, tools=TOOLS)
        choice = response.choices[0].message

        structured: dict = {}
        if choice.tool_calls:
            messages.append(choice.model_dump(exclude_none=True))
            for tool_call in choice.tool_calls:
                result, payload = run_tool(tool_call.function.name, tool_call.function.arguments, category_slug)
                if payload is not None:
                    structured.update(payload)
                messages.append(
                    {"role": "tool", "tool_call_id": tool_call.id, "content": str(result)}
                )
            response = client.chat.completions.create(model=CHAT_MODEL, messages=messages)
            choice = response.choices[0].message

        return {"reply": choice.content, **structured}
