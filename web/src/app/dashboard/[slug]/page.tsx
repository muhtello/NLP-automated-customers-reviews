"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

type ProductStat = {
  name: string;
  avg_rating: number;
  review_count: number;
  pct_negative: number;
  sample_complaints: string[];
};

type CategorySummary = {
  slug: string;
  stats: {
    category: string;
    top_products: ProductStat[];
    worst_product: ProductStat | null;
  };
  article: string;
};

export default function CategoryDetail() {
  const params = useParams<{ slug: string }>();
  const slug = params.slug;
  const [summary, setSummary] = useState<CategorySummary | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!slug) return;
    fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/categories/${slug}`)
      .then((response) => {
        if (!response.ok) throw new Error(`Request failed: ${response.status}`);
        return response.json();
      })
      .then((data) => {
        setSummary(data);
        setError("");
      })
      .catch(() => {
        setError("Could not load this category. Is the API running on port 8000?");
        setSummary(null);
      });
  }, [slug]);

  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-6 p-6">
      <Link href="/dashboard" className="text-sm text-blue-600 hover:underline">
        &larr; Back to dashboard
      </Link>

      {error && <p className="text-red-600">{error}</p>}
      {!summary && !error && <p>Loading...</p>}

      {summary && (
        <>
          <h1 className="text-2xl font-semibold">{summary.stats.category}</h1>

          <article className="prose whitespace-pre-wrap text-sm leading-relaxed">{summary.article}</article>

          <section>
            <h2 className="mb-2 text-lg font-medium">Top products</h2>
            <ul className="flex flex-col gap-2">
              {summary.stats.top_products.map((product) => (
                <li key={product.name} className="rounded border border-gray-200 p-3">
                  <p className="font-medium">{product.name}</p>
                  <p className="text-sm text-gray-500">
                    {product.avg_rating.toFixed(2)} avg rating &middot; {product.review_count} reviews &middot;{" "}
                    {(product.pct_negative * 100).toFixed(1)}% negative
                  </p>
                </li>
              ))}
            </ul>
          </section>

          {summary.stats.worst_product && (
            <section>
              <h2 className="mb-2 text-lg font-medium">One to avoid</h2>
              <div className="rounded border border-red-200 bg-red-50 p-3">
                <p className="font-medium">{summary.stats.worst_product.name}</p>
                <p className="text-sm text-gray-500">
                  {summary.stats.worst_product.avg_rating.toFixed(2)} avg rating &middot;{" "}
                  {summary.stats.worst_product.review_count} reviews
                </p>
              </div>
            </section>
          )}
        </>
      )}
    </div>
  );
}
