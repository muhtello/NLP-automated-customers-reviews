"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

import ArticleBody from "@/components/ArticleBody/ArticleBody";
import CategoryIcon from "@/components/CategoryIcon/CategoryIcon";
import ProductThumb from "@/components/ProductThumb/ProductThumb";
import VerdictBadge from "@/components/VerdictBadge/VerdictBadge";

type ProductStat = {
  name: string;
  avg_rating: number;
  review_count: number;
  pct_negative: number;
  image_url: string | null;
};

type CategorySummary = {
  slug: string;
  stats: {
    category: string;
    total_reviews: number;
    avg_rating: number;
    pct_negative: number;
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
        setError("This category is not on file. Is the API running on port 8000?");
        setSummary(null);
      });
  }, [slug]);

  return (
    <div className="flex flex-col gap-6">
      <Link href="/dashboard" className="w-fit text-xs font-medium text-secondary transition-colors hover:text-primary">
        &larr; Back to dashboard
      </Link>

      {error && <p className="text-sm text-negative-strong">{error}</p>}
      {!summary && !error && <p className="font-mono text-xs uppercase tracking-widest text-ink-faint">Loading category...</p>}

      {summary && (
          <div className="grid grid-cols-1 gap-8 lg:grid-cols-[280px_1fr]">
            {/* Sticky sidebar: metadata */}
            <aside className="flex flex-col gap-5 lg:sticky lg:top-8 lg:self-start">
              <div className="flex items-center gap-3">
                <span className="flex h-11 w-11 items-center justify-center rounded bg-primary-soft text-primary">
                  <CategoryIcon slug={slug} className="h-6 w-6" />
                </span>
                <h1 className="text-xl font-semibold tracking-tight text-ink">{summary.stats.category}</h1>
              </div>

              <VerdictBadge avgRating={summary.stats.avg_rating} pctNegative={summary.stats.pct_negative} size="lg" animate />

              <dl className="flex flex-col gap-3 rounded border border-line bg-surface p-4 text-sm">
                <div className="flex items-center justify-between">
                  <dt className="text-ink-soft">Reviews on file</dt>
                  <dd className="font-mono font-semibold text-ink">{summary.stats.total_reviews.toLocaleString()}</dd>
                </div>
                <div className="flex items-center justify-between border-t border-line pt-3">
                  <dt className="text-ink-soft">Negative rate</dt>
                  <dd className="font-mono font-semibold text-negative-strong">
                    {(summary.stats.pct_negative * 100).toFixed(1)}%
                  </dd>
                </div>
              </dl>
            </aside>

            {/* Main column: article + products */}
            <div className="flex flex-col gap-8">
              <section className="glass-panel rounded p-6">
                <span className="mb-3 flex items-center gap-1.5 font-mono text-[10px] font-semibold uppercase tracking-widest text-primary">
                  <span className="h-1.5 w-1.5 animate-pulse-dot rounded-full bg-primary" />
                  AI-generated summary
                </span>
                <ArticleBody text={summary.article} />
              </section>

              <section className="flex flex-col gap-3">
                <h2 className="text-sm font-semibold uppercase tracking-widest text-ink-soft">Top products</h2>
                <div className="flex flex-col divide-y divide-line rounded border border-line bg-surface">
                  {summary.stats.top_products.map((product, index) => (
                    <div key={product.name} className="flex items-center gap-4 p-4">
                      <span className="w-6 shrink-0 font-mono text-sm font-semibold text-ink-faint">
                        {String(index + 1).padStart(2, "0")}
                      </span>
                      <ProductThumb imageUrl={product.image_url} categorySlug={slug} alt={product.name} />
                      <div className="flex flex-1 flex-col gap-1">
                        <p className="text-sm font-medium text-ink">{product.name}</p>
                        <div className="flex items-center gap-2">
                          <div className="h-1 w-32 overflow-hidden rounded-full bg-neutral-soft">
                            <div className="h-full bg-positive" style={{ width: `${(product.avg_rating / 5) * 100}%` }} />
                          </div>
                          <span className="font-mono text-xs text-ink-faint">
                            {product.avg_rating.toFixed(2)} &middot; {product.review_count} reviews
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </section>

              {summary.stats.worst_product && (
                <section className="flex flex-col gap-3">
                  <h2 className="text-sm font-semibold uppercase tracking-widest text-negative-strong">Worst rated</h2>
                  <div className="flex items-center gap-4 rounded border border-negative/20 bg-negative-soft p-4">
                    <ProductThumb
                      imageUrl={summary.stats.worst_product.image_url}
                      categorySlug={slug}
                      alt={summary.stats.worst_product.name}
                      size="sm"
                    />
                    <p className="flex-1 text-sm font-medium text-ink">{summary.stats.worst_product.name}</p>
                    <span className="font-mono text-xs text-ink-faint">
                      {summary.stats.worst_product.avg_rating.toFixed(2)} &middot; {summary.stats.worst_product.review_count} reviews
                    </span>
                  </div>
                </section>
              )}
            </div>
          </div>
        )}
    </div>
  );
}
