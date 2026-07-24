"""Tests for src/chatbot_engine.py's branching logic, with a fake OpenAI client.

Real model calls aren't available in this environment, so these verify the code's own
behavior (tool-call handling, persona selection, summary caching) given scripted
responses, not whether gpt-4o-mini picks the right tool for a given phrasing.
"""

import json
from types import SimpleNamespace

from src.chatbot_engine import PERSONA_PROMPTS, PERSONA_REMINDERS, SUMMARY_TRIGGER_LENGTH, ChatEngine
from src.schemas import ChatMessage


def _message(content: str | None = None, tool_calls: list | None = None) -> SimpleNamespace:
    return SimpleNamespace(
        content=content,
        tool_calls=tool_calls,
        model_dump=lambda exclude_none=True: {"role": "assistant", "content": content},
    )


def _tool_call(name: str, arguments: dict, call_id: str = "call_1") -> SimpleNamespace:
    return SimpleNamespace(id=call_id, function=SimpleNamespace(name=name, arguments=json.dumps(arguments)))


class FakeClient:
    """Records every messages= payload it's called with and replays scripted responses in order."""

    def __init__(self, messages_in_order: list[SimpleNamespace]) -> None:
        self._queue = list(messages_in_order)
        self.calls: list[dict] = []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        message = self._queue.pop(0)
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def _engine_with(fake_client: FakeClient) -> ChatEngine:
    engine = ChatEngine()
    engine._client = fake_client
    return engine


def test_reply_without_tool_call_returns_content_directly() -> None:
    fake_client = FakeClient([_message(content="Hi there")])
    engine = _engine_with(fake_client)

    result = engine.reply("hello", None, [], mode="recommender")

    assert result["reply"] == "Hi there"
    assert result["summary"] is None
    assert len(fake_client.calls) == 1


def test_recommender_and_anti_recommender_get_different_system_prompts() -> None:
    fake_client = FakeClient([_message(content="ok"), _message(content="ok")])
    engine = _engine_with(fake_client)

    engine.reply("hello", None, [], mode="recommender")
    engine.reply("hello", None, [], mode="anti_recommender")

    first_system_prompt = fake_client.calls[0]["messages"][0]["content"]
    second_system_prompt = fake_client.calls[1]["messages"][0]["content"]
    assert first_system_prompt != second_system_prompt
    assert PERSONA_PROMPTS["recommender"] in first_system_prompt
    assert PERSONA_PROMPTS["anti_recommender"] in second_system_prompt


def test_reply_handles_tool_call_and_category_hint_handoff() -> None:
    """Simulates the 'audio product' scenario: a lookup_product tool call misses by name,
    and the resulting tool message should carry the category hint for the model to act on."""
    fake_client = FakeClient(
        [
            _message(tool_calls=[_tool_call("lookup_product", {"name": "audio product"})]),
            _message(content="Here are some audio products."),
        ]
    )
    engine = _engine_with(fake_client)

    result = engine.reply("audio product", None, [], mode="recommender")

    assert result["reply"] == "Here are some audio products."
    assert len(fake_client.calls) == 2
    final_messages = fake_client.calls[1]["messages"]
    tool_message = next(message for message in final_messages if message["role"] == "tool")
    assert "matched_category" in tool_message["content"]
    # The persona reminder should be the last message before the final completion call, so it
    # has the most influence over tone even after tool data has entered the context.
    assert final_messages[-1]["role"] == "system"


def test_persona_reminder_differs_by_mode_after_a_tool_call() -> None:
    fake_client = FakeClient(
        [
            _message(tool_calls=[_tool_call("rank_products", {"order": "best", "limit": 3, "category": "all"})]),
            _message(content="ok"),
        ]
    )
    engine = _engine_with(fake_client)
    engine.reply("give me the best products", None, [], mode="anti_recommender")

    reminder = fake_client.calls[1]["messages"][-1]["content"]
    assert PERSONA_REMINDERS["anti_recommender"] == reminder


def test_reply_reuses_existing_summary_without_extra_call() -> None:
    fake_client = FakeClient([_message(content="ok")])
    engine = _engine_with(fake_client)
    history = [ChatMessage(role="user", content="hi"), ChatMessage(role="assistant", content="hello")]

    result = engine.reply("follow up", None, history, mode="recommender", summary="earlier summary")

    assert result["summary"] == "earlier summary"
    assert len(fake_client.calls) == 1


def test_reply_regenerates_summary_once_history_crosses_trigger() -> None:
    fake_client = FakeClient([_message(content="new summary text"), _message(content="final reply")])
    engine = _engine_with(fake_client)
    history = [ChatMessage(role="user", content=f"message {i}") for i in range(SUMMARY_TRIGGER_LENGTH)]

    result = engine.reply("follow up", None, history, mode="recommender")

    assert result["summary"] == "new summary text"
    assert result["reply"] == "final reply"
    assert len(fake_client.calls) == 2
