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
        "You are an enthusiastic, encouraging shopping assistant. In every reply, lead with what "
        "reviewers loved, use upbeat language, and end on a confident buy-it recommendation when the "
        "data supports it. Never adopt a sarcastic or discouraging tone — that is a different persona."
    ),
    "anti_recommender": (
        "You are a sarcastic, skeptical anti-shopping assistant. In every reply, your goal is to talk "
        "the user OUT of buying — lead with complaints, flaws, and buyer's remorse from the reviews, "
        "use dry/sarcastic wording, and end by discouraging the purchase or suggesting they reconsider. "
        "Never sound enthusiastic or encouraging about buying — that is a different persona. Stay "
        "sarcastic and critical even if the average rating is high: dig for the negative reviews and "
        "lean on those."
    ),
}

# Re-asserted right before the final answer, only on turns where a tool call injected factual
# rating data into the context. That data sits closer to the end of the message list than the
# original persona instruction, and models weight recent context more heavily — without this
# reminder, both personas tend to flatten into the same neutral, data-reporting tone.
PERSONA_REMINDERS = {
    "recommender": (
        "Reminder before you answer: stay in the enthusiastic, encouraging persona — lead with what "
        "reviewers loved and end on a confident buy-it recommendation, even though you just saw factual "
        "rating data. Do not sound neutral, sarcastic, or discouraging."
    ),
    "anti_recommender": (
        "Reminder before you answer: stay in the sarcastic, skeptical persona — lead with complaints and "
        "reasons to hesitate, even though the data you just saw may show high ratings. Do not sound "
        "neutral, enthusiastic, or encouraging."
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
            "and rank the best/worst products for a category. Call them whenever the user names a "
            "product or asks about a kind/type of product, instead of guessing. A general product "
            "type or category (e.g. 'audio product', 'headphones', 'tablets') is NOT a specific "
            "product — use the ranking tool for those, not the single-product lookup tools. If a "
            "lookup tool returns a matched_category hint, immediately call the ranking tool with that "
            "category rather than reporting a dead end. If a tool reports the product or category was "
            "genuinely not found (no hint given), say plainly that you don't have related products for "
            "that — never substitute a different product/category or invent data to fill the gap."
        )
        return persona + context + tool_guidance

    def _condensed_history(
        self, client: OpenAI, history: list[ChatMessage], existing_summary: str | None
    ) -> tuple[list[dict], str | None]:
        """Returns (messages to send, summary to echo back on the next request).

        If the caller already holds a summary of earlier turns and hasn't sent enough new
        messages to warrant refreshing it, that summary is reused as-is instead of paying for
        another summarization call on every single turn.
        """
        if existing_summary is not None and len(history) < SUMMARY_TRIGGER_LENGTH:
            condensed = [{"role": "system", "content": f"Earlier conversation summary: {existing_summary}"}]
            condensed += [{"role": entry.role, "content": entry.content} for entry in history]
            return condensed, existing_summary

        if len(history) < SUMMARY_TRIGGER_LENGTH:
            return [{"role": entry.role, "content": entry.content} for entry in history], existing_summary

        older, recent = history[:-KEEP_RECENT_MESSAGES], history[-KEEP_RECENT_MESSAGES:]
        transcript = "\n".join(f"{entry.role}: {entry.content}" for entry in older)
        if existing_summary is not None:
            transcript = f"Previous summary: {existing_summary}\n\n{transcript}"
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
        return condensed, summary_text

    def reply(
        self,
        message: str,
        category_slug: str | None,
        history: list[ChatMessage],
        mode: str = "recommender",
        summary: str | None = None,
    ) -> dict:
        client = self._client_or_raise()
        system_prompt = self._build_system_prompt(category_slug, mode)

        condensed_history, next_summary = self._condensed_history(client, history, summary)
        messages = [{"role": "system", "content": system_prompt}]
        messages += condensed_history
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
            reminder = PERSONA_REMINDERS.get(mode, PERSONA_REMINDERS["recommender"])
            messages.append({"role": "system", "content": reminder})
            response = client.chat.completions.create(model=CHAT_MODEL, messages=messages)
            choice = response.choices[0].message

        return {"reply": choice.content, "summary": next_summary, **structured}
