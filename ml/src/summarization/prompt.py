"""Builds the LLM prompt that turns aggregated category stats into an article."""

_PROMPT_TEMPLATE = """You are a product-review editor writing a short recommendation \
article for the "{category}" category on an e-commerce site.

Use only the data below - do not invent products, ratings, or complaints.

TOP {top_count} PRODUCTS (by average rating):
{top_products_block}

PRODUCT TO AVOID:
{worst_product_block}

Write a short blog-post-style article (roughly 250-400 words) with this structure:
1. A one-sentence intro naming the category.
2. "Top Picks" - introduce the top products, compare their average ratings and \
review counts, and call out the key differences between them based on what \
reviewers say in the complaint samples (or their absence).
3. "What Reviewers Complain About" - for each top product, a short bullet or \
sentence summarizing recurring complaint themes from its sample complaints \
(if none are listed, say reviewers had few complaints).
4. "One to Avoid" - name the worst-rated product, its average rating, and \
explain why to avoid it based on its sample complaints.

Keep the tone helpful and factual, not salesy. Do not fabricate details beyond \
what's given.
"""

_PRODUCT_BLOCK_TEMPLATE = """- {name}
  avg_rating: {avg_rating} / 5.0 ({review_count} reviews, {pct_negative:.0%} negative)
  sample complaints: {complaints}"""


def _format_product_block(product: dict) -> str:
    complaints = product["sample_complaints"]
    complaints_text = " | ".join(complaints) if complaints else "(none recorded)"
    return _PRODUCT_BLOCK_TEMPLATE.format(
        name=product["name"],
        avg_rating=product["avg_rating"],
        review_count=product["review_count"],
        pct_negative=product["pct_negative"],
        complaints=complaints_text,
    )


def build_prompt(category_stats: dict) -> str:
    top_products = category_stats["top_products"]
    worst_product = category_stats["worst_product"]

    top_products_block = "\n".join(_format_product_block(p) for p in top_products) or "(no eligible products)"
    worst_product_block = _format_product_block(worst_product) if worst_product else "(no eligible product found)"

    return _PROMPT_TEMPLATE.format(
        category=category_stats["category"],
        top_count=len(top_products),
        top_products_block=top_products_block,
        worst_product_block=worst_product_block,
    )
