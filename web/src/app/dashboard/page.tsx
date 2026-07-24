"use client";

import CategoryCard from "@/components/CategoryCard/CategoryCard";
import { useCategories } from "@/lib/useCategories";

export default function Dashboard() {
  const { categories, error } = useCategories();
  const totalReviews = categories.reduce((sum, item) => sum + item.total_reviews, 0);
  const weightedNegative =
    totalReviews > 0 ? categories.reduce((sum, item) => sum + item.pct_negative * item.total_reviews, 0) / totalReviews : 0;
  const topCategory = [...categories].sort((a, b) => b.avg_rating - a.avg_rating)[0];

  if (error) {
    return (
      <p className="rounded border border-dashed border-negative bg-negative-soft p-4 text-sm text-negative-strong">
        {error} Start it with <code className="font-mono">uvicorn src.main:app --reload</code> from the{" "}
        <code className="font-mono">api/</code> directory.
      </p>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <div className="rounded-xl border border-line bg-surface p-5">
          <p className="text-xs uppercase tracking-widest text-ink-faint">Total reviews analyzed</p>
          <p className="mt-2 font-mono text-3xl font-semibold text-primary">{totalReviews.toLocaleString()}</p>
        </div>
        <div className="rounded-xl border border-line bg-surface p-5">
          <p className="text-xs uppercase tracking-widest text-ink-faint">Top-rated category</p>
          <p className="mt-2 text-lg font-semibold text-ink">{topCategory ? topCategory.category : "—"}</p>
          {topCategory && <p className="font-mono text-sm text-ink-soft">{topCategory.avg_rating.toFixed(2)} avg rating</p>}
        </div>
        <div className="rounded-xl border border-line bg-surface p-5">
          <p className="text-xs uppercase tracking-widest text-ink-faint">Overall negative rate</p>
          <div className="mt-2 flex items-center gap-3">
            <span className="font-mono text-3xl font-semibold text-negative-strong">{(weightedNegative * 100).toFixed(1)}%</span>
            <div className="h-2 flex-1 overflow-hidden rounded-full bg-neutral-soft">
              <div className="h-full bg-negative" style={{ width: `${weightedNegative * 100}%` }} />
            </div>
          </div>
        </div>
      </div>

      <div className="flex flex-col gap-3">
        <h2 className="text-sm font-semibold uppercase tracking-widest text-ink-soft">
          {categories.length === 0 ? "Loading categories..." : `${categories.length} product categories`}
        </h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {categories.map((item) => (
            <CategoryCard
              key={item.slug}
              item={item}
              shareOfTotal={totalReviews > 0 ? (item.total_reviews / totalReviews) * 100 : 0}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
