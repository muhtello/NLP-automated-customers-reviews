# Dataset Overview — Automated Customer Reviews Project

## Data Sources
Three raw Amazon product review exports (Datafiniti) were combined:

| File | Rows | Unique Products |
|---|---|---|
| `1429_1.csv` | 34,660 | 42 |
| `Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv` | 5,000 | 24 |
| `Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv` | 28,332 | 65 |

The three files overlapped significantly (the same reviews appeared across multiple files), but each also contained unique reviews not present in the others. We merged all three, kept only the columns relevant to our NLP tasks, and removed duplicate reviews (same product + review text + rating).

## Final Merged Dataset

- **59,743 total unique reviews**
- **89 unique product IDs**
- **119 unique product names** — more names than IDs, which is normal in Amazon-style data (the same product ID can have slightly different name strings across listings, e.g. different variants/bundles of the same product)
- **7 unique brands only** — this dataset is fairly narrow, dominated by Amazon-brand devices (Kindles, Fire tablets, Echo, chargers/batteries, etc.), not a broad general product catalog

## Data Quality Issue Found: `id` and `name` Fields

While investigating the id/name mismatch, we found a real data quality problem, not just normal variation:

- Some `name` values are **corrupted** — two unrelated product names are concatenated together in the same field (a known artifact of this export format)
- In several cases, the **same `id` is attached to genuinely different products** (e.g. one `id` covered an Echo, a Fire Tablet, a Kindle cover, a USB charger, and even "Coconut Water Red Tea")
- This affected **21 of 89 product IDs (~11% of all reviews)**

**Fix applied:** cleaned the `name` field (kept only the first product name segment) and treated `id` as unreliable going forward — using the cleaned product name as the trusted identifier for grouping and analysis instead.

## Product Categorization (Objective 2)

After cleaning, we grouped the 106 distinct cleaned product names into **5 meta-categories**, combining text-based clustering (TF-IDF + KMeans) with rule-based logic informed by the (partially available but accurate) `primaryCategories` field:

| Category | Products | Reviews |
|---|---|---|
| Tablets | 40 | 29,553 |
| Accessories & Chargers | 19 | 11,126 |
| Smart Home & Speakers | 23 | 7,665 |
| E-Readers | 17 | 4,631 |
| Non-Electronics | 7 | 9 |

## Key Takeaways for the Team

1. The dataset is **narrow in scope** (7 brands, mostly Amazon devices) rather than a general product catalog — worth keeping in mind when interpreting results.
2. The `id` field **cannot be trusted on its own** for product identification; a cleaned product name is the more reliable key.
3. Review volume is **heavily skewed toward Tablets** (~49% of all reviews), with Non-Electronics being a very small edge case (7 products, 9 reviews total) — likely not enough data to draw meaningful conclusions for that category alone.
4. Star ratings are also **imbalanced toward 5-star reviews** (~69% of the dataset), which is being accounted for in the sentiment classification modeling (Objective 1).
