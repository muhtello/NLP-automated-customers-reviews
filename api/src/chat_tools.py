"""OpenAI function-calling tools that let the chatbot query the review dataset directly.

Each tool wraps a src/products.py lookup. `run_tool` returns (result_for_llm, structured_payload) —
structured_payload is None unless the frontend should render a table/list for this call.
"""

import json

from src.products import find_product, get_product_comparison, rank_products, resolve_category

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_product",
            "description": (
                "Check whether ONE specific, named product exists in the review dataset (e.g. 'Kindle "
                "Paperwhite', 'Echo Dot'). Do NOT use this for a general product type/category (e.g. "
                "'audio product', 'headphones', 'tablets') — use rank_products for those instead, since "
                "there's no single product named after a category."
            ),
            "parameters": {
                "type": "object",
                "properties": {"name": {"type": "string", "description": "Product name as the user wrote it."}},
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compare_product_reviews",
            "description": (
                "Get the best-rated and worst-rated review on file for ONE specific, named product, so it "
                "can be shown as a side-by-side comparison. Do NOT use this for a general product type/"
                "category — use rank_products for those instead."
            ),
            "parameters": {
                "type": "object",
                "properties": {"name": {"type": "string", "description": "Product name as the user wrote it."}},
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "rank_products",
            "description": (
                "List the best- or worst-rated products for a category or general product type (e.g. "
                "'audio product', 'headphones', 'tablets', 'e-readers'). Use this whenever the user asks "
                "about a kind/type of product rather than one exact named product — it's also how you "
                "answer 'what audio products do you have'. If the tool reports the category wasn't found, "
                "that means the dataset has no matching products — tell the user that rather than "
                "substituting a different category or ranking across everything."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "order": {"type": "string", "enum": ["best", "worst"]},
                    "limit": {"type": "integer", "description": "How many products to return, e.g. 5."},
                    "category": {
                        "type": "string",
                        "description": (
                            "The category the user means, in their own words (e.g. 'pets', 'e-readers', "
                            "'tablets'). Pass 'current' to mean the category currently open in the dashboard, "
                            "or 'all' only if the user explicitly wants no category filter."
                        ),
                    },
                },
                "required": ["order", "limit", "category"],
            },
        },
    },
]


def _not_found_with_category_hint(queried_name: str) -> dict:
    """Called when a specific-product lookup misses — often because the user actually meant a
    category/type of product (e.g. 'audio product'), not one exact item. If the name resolves to a
    known category, surface that so the model calls rank_products instead of reporting a dead end.
    """
    category_slug = resolve_category(queried_name)
    if category_slug is None:
        return {"found": False, "tool_error": True}
    return {
        "found": False,
        "tool_error": True,
        "note": (
            f"'{queried_name}' isn't a specific product, but it matches the category "
            f"'{category_slug}'. Call rank_products with that category instead of reporting not found."
        ),
        "matched_category": category_slug,
    }


def run_tool(tool_name: str, arguments_json: str, category_slug: str | None) -> tuple[dict, dict | None]:
    args = json.loads(arguments_json or "{}")

    if tool_name == "lookup_product":
        product = find_product(args["name"])
        if product is None:
            return _not_found_with_category_hint(args["name"]), None
        return {"found": True, **product}, None

    if tool_name == "compare_product_reviews":
        comparison = get_product_comparison(args["name"])
        if comparison is None:
            return _not_found_with_category_hint(args["name"]), None
        return comparison, {"product_comparison": comparison}

    if tool_name == "rank_products":
        category_query = args.get("category", "current")
        if category_query == "all":
            slug = None
        elif category_query == "current":
            if category_slug is None:
                return {"found_category": False, "tool_error": True}, None
            slug = category_slug
        else:
            slug = resolve_category(category_query)
            if slug is None:
                return {"found_category": False, "tool_error": True}, None

        ranking = rank_products(slug, args["order"], int(args["limit"]))
        return ranking, {"product_ranking": ranking}

    return {"error": f"Unknown tool '{tool_name}'"}, None
