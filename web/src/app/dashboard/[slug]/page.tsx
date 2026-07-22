"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

import ArticleBody from "@/components/ArticleBody/ArticleBody";
import CategoryIcon from "@/components/CategoryIcon/CategoryIcon";
import ProductThumb from "@/components/ProductThumb/ProductThumb";
import StampBadge from "@/components/StampBadge/StampBadge";

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
        setError("This entry is not on file. Is the API running on port 8000?");
        setSummary(null);
      });
  }, [slug]);

  return (
    <div className="min-h-screen">
      <header className="border-b border-line bg-ledger px-6 py-4 text-paper">
        <div className="mx-auto max-w-3xl">
          <Link href="/dashboard" className="font-display text-xs uppercase tracking-widest text-paper/80 hover:text-paper hover:underline">
            &larr; Back to ledger
          </Link>
        </div>
      </header>

      <main className="mx-auto flex max-w-3xl flex-col gap-8 p-6">
        {error && <p className="text-sm text-stamp-red">{error}</p>}
        {!summary && !error && <p className="font-display text-xs uppercase tracking-widest text-ink-soft">Pulling entry...</p>}

        {summary && (
          <>
            <section className="flex items-start justify-between gap-6 border-b border-dashed border-line pb-6">
              <div className="flex flex-col gap-2">
                <span className="font-display text-[11px] uppercase tracking-[0.2em] text-ink-soft">
                  Manifest entry &middot; {summary.stats.total_reviews.toLocaleString()} reviews on file
                </span>
                <h1 className="flex items-center gap-3 font-display text-2xl font-semibold tracking-tight text-ink">
                  <CategoryIcon slug={slug} className="h-7 w-7 text-ledger" />
                  {summary.stats.category}
                </h1>
                <p className="font-display text-xs uppercase tracking-wide text-ink-soft">
                  Negative rate {(summary.stats.pct_negative * 100).toFixed(1)}%
                </p>
              </div>
              <StampBadge avgRating={summary.stats.avg_rating} pctNegative={summary.stats.pct_negative} size="lg" animate />
            </section>

            <section className="rounded-sm border-l-2 border-ledger bg-paper-raised p-6">
              <ArticleBody text={summary.article} />
            </section>

            <section className="flex flex-col gap-3">
              <h2 className="font-display text-sm font-semibold uppercase tracking-widest text-ink-soft">Top products</h2>
              {summary.stats.top_products.map((product, index) => (
                <div key={product.name} className="flex items-center gap-4 border-b border-line py-3 last:border-none">
                  <span className="w-6 shrink-0 font-display text-sm font-semibold text-ink-soft">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <ProductThumb imageUrl={product.image_url} categorySlug={slug} alt={product.name} />
                  <div className="flex flex-1 flex-col gap-1">
                    <p className="text-sm font-medium text-ink">{product.name}</p>
                    <div className="flex items-center gap-2">
                      <div className="h-1.5 w-32 overflow-hidden rounded-full bg-line">
                        <div className="h-full bg-stamp-green" style={{ width: `${(product.avg_rating / 5) * 100}%` }} />
                      </div>
                      <span className="font-display text-xs text-ink-soft">
                        {product.avg_rating.toFixed(2)} &middot; {product.review_count} reviews
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </section>

            {summary.stats.worst_product && (
              <section className="flex flex-col gap-2">
                <h2 className="font-display text-sm font-semibold uppercase tracking-widest text-stamp-red">Flagged for return</h2>
                <div className="flex items-center gap-4 border-l-2 border-stamp-red bg-paper-raised p-4">
                  <ProductThumb
                    imageUrl={summary.stats.worst_product.image_url}
                    categorySlug={slug}
                    alt={summary.stats.worst_product.name}
                    size="sm"
                  />
                  <p className="flex-1 text-sm font-medium text-ink">{summary.stats.worst_product.name}</p>
                  <span className="font-display text-xs text-ink-soft">
                    {summary.stats.worst_product.avg_rating.toFixed(2)} &middot; {summary.stats.worst_product.review_count} reviews
                  </span>
                </div>
              </section>
            )}
          </>
        )}
      </main>
    </div>
  );
}
