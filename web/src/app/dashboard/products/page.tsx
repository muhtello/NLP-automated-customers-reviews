"use client";

import { useState } from "react";

import ProductAnalysis from "@/components/ProductAnalysis/ProductAnalysis";
import { useProductSearch } from "@/lib/useProductSearch";

export default function Products() {
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState<string | null>(null);
  const { products, error } = useProductSearch(query);

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-[1fr_420px]">
      <div className="flex flex-col gap-4">
        <div>
          <h2 className="text-base font-semibold text-ink">Browse products</h2>
          <p className="text-sm text-ink-soft">Search by product name, then pick one to run the sentiment model on its reviews.</p>
        </div>

        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search products (e.g. Kindle, Echo, batteries)..."
          className="rounded border border-line bg-surface px-3 py-2 text-sm text-ink outline-none transition-colors focus:border-2 focus:border-primary"
        />

        {error && <p className="text-sm text-negative-strong">{error}</p>}

        <div className="flex flex-col divide-y divide-line rounded border border-line bg-surface">
          {products.length === 0 && !error && (
            <p className="p-4 text-sm text-ink-faint">
              {query.trim() === "" ? "Start typing to search products." : "No products match that search."}
            </p>
          )}
          {products.map((product) => (
            <button
              key={product.name}
              onClick={() => setSelected(product.name)}
              className={`flex items-center justify-between gap-4 p-4 text-left transition-colors hover:bg-surface-sunken ${
                selected === product.name ? "bg-primary-soft" : ""
              }`}
            >
              <span className="text-sm font-medium text-ink">{product.name}</span>
              <span className="shrink-0 font-mono text-xs text-ink-faint">
                {product.review_count.toLocaleString()} reviews &middot; {product.avg_rating.toFixed(2)} avg
              </span>
            </button>
          ))}
        </div>
      </div>

      <div className="lg:sticky lg:top-24 lg:self-start">
        {selected ? (
          <ProductAnalysis productName={selected} />
        ) : (
          <div className="rounded-xl border border-dashed border-line p-5 text-sm text-ink-faint">
            Select a product from the list to analyze its reviews.
          </div>
        )}
      </div>
    </div>
  );
}
