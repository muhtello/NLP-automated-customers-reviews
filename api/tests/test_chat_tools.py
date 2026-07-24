"""Tests for src/chat_tools.py's dispatch logic, no OpenAI client involved.

These check the structural contract the LLM relies on: not-found results carry a
`tool_error` flag, and a specific-product miss that's really a category query surfaces
a `matched_category` hint instead of a flat dead end.
"""

import json

from src.chat_tools import run_tool


def test_lookup_product_hit_has_no_tool_error() -> None:
    result, payload = run_tool("lookup_product", json.dumps({"name": "Fire Tablet"}), None)
    assert result["found"] is True
    assert "tool_error" not in result
    assert payload is None


def test_lookup_product_category_query_gets_hint() -> None:
    """A general product type ('audio product') should miss the name lookup but hint at
    the category it resolves to, so the model can call rank_products instead of stopping."""
    result, payload = run_tool("lookup_product", json.dumps({"name": "audio product"}), None)
    assert result["found"] is False
    assert result["tool_error"] is True
    assert result["matched_category"] == "smart-home-audio-systems"
    assert payload is None


def test_lookup_product_genuine_miss_has_tool_error_and_no_hint() -> None:
    result, _ = run_tool("lookup_product", json.dumps({"name": "nonexistentxyz123"}), None)
    assert result == {"found": False, "tool_error": True}


def test_rank_products_unknown_category_has_tool_error() -> None:
    result, payload = run_tool(
        "rank_products", json.dumps({"order": "best", "limit": 5, "category": "nonexistentxyz123"}), None
    )
    assert result == {"found_category": False, "tool_error": True}
    assert payload is None


def test_rank_products_current_with_no_category_selected_has_tool_error() -> None:
    result, _ = run_tool("rank_products", json.dumps({"order": "best", "limit": 5, "category": "current"}), None)
    assert result == {"found_category": False, "tool_error": True}


def test_rank_products_synonym_category_resolves() -> None:
    """'speakers' has no word overlap with the audio category slug/label, so this only
    works via the synonym map in src/products.py's resolve_category."""
    result, payload = run_tool(
        "rank_products", json.dumps({"order": "best", "limit": 3, "category": "speakers"}), None
    )
    assert result["category"] is not None
    assert payload is not None
