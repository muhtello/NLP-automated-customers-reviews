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
            "description": "Check whether a specific product exists in the review dataset and get its basic stats.",
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
                "Get the best-rated and worst-rated review on file for one product, so it can be "
                "shown as a side-by-side comparison."
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
                "List the best- or worst-rated products for a category. If the tool reports the category "
                "wasn't found, that means the dataset has no matching products — tell the user that rather "
                "than substituting a different category or ranking across everything."
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


def run_tool(tool_name: str, arguments_json: str, category_slug: str | None) -> tuple[dict, dict | None]:
    args = json.loads(arguments_json or "{}")

    if tool_name == "lookup_product":
        product = find_product(args["name"])
        if product is None:
            return {"found": False}, None
        return {"found": True, **product}, None

    if tool_name == "compare_product_reviews":
        comparison = get_product_comparison(args["name"])
        if comparison is None:
            return {"found": False}, None
        return comparison, {"product_comparison": comparison}

    if tool_name == "rank_products":
        category_query = args.get("category", "current")
        if category_query == "all":
            slug = None
        elif category_query == "current":
            if category_slug is None:
                return {"found_category": False}, None
            slug = category_slug
        else:
            slug = resolve_category(category_query)
            if slug is None:
                return {"found_category": False}, None

        ranking = rank_products(slug, args["order"], int(args["limit"]))
        return ranking, {"product_ranking": ranking}

    return {"error": f"Unknown tool '{tool_name}'"}, None
