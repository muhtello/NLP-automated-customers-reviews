"use client";

import Link from "next/link";

import CategoryCard from "@/components/CategoryCard/CategoryCard";
import { useCategories } from "@/lib/useCategories";

export default function Dashboard() {
  const { categories, error } = useCategories();
  const totalReviews = categories.reduce((sum, item) => sum + item.total_reviews, 0);

  return (
    <div className="min-h-screen bg-bg">
      <header className="border-b border-line bg-surface px-6 py-4">
        <div className="mx-auto flex max-w-[1440px] items-center justify-between">
          <div className="flex items-center gap-2.5">
            <span className="flex h-8 w-8 items-center justify-center rounded bg-primary text-sm font-semibold text-white">S</span>
            <div className="flex flex-col leading-tight">
              <span className="text-sm font-semibold text-ink">Signal</span>
              <span className="font-mono text-[10px] uppercase tracking-widest text-ink-faint">Category dashboard</span>
            </div>
          </div>
          <Link
            href="/"
            className="rounded border border-line px-3 py-1.5 text-xs font-medium text-secondary transition-colors hover:border-primary/30 hover:text-primary"
          >
            Sentiment checker &rarr;
          </Link>
        </div>
      </header>

      <main className="mx-auto flex max-w-[1440px] flex-col gap-6 px-6 py-8">
        <div className="flex flex-col gap-1">
          <h1 className="text-2xl font-semibold tracking-tight text-ink">Product categories</h1>
          <p className="font-mono text-xs uppercase tracking-widest text-ink-faint">
            {error
              ? "Dashboard unreachable"
              : categories.length === 0
                ? "Loading categories..."
                : `${totalReviews.toLocaleString()} reviews classified · ${categories.length} categories`}
          </p>
        </div>

        {error && (
          <p className="rounded border border-dashed border-negative bg-negative-soft p-4 text-sm text-negative-strong">
            {error} Start it with <code className="font-mono">uvicorn src.main:app --reload</code> from the{" "}
            <code className="font-mono">api/</code> directory.
          </p>
        )}

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {categories.map((item) => (
            <CategoryCard
              key={item.slug}
              item={item}
              shareOfTotal={totalReviews > 0 ? (item.total_reviews / totalReviews) * 100 : 0}
            />
          ))}
        </div>
      </main>
    </div>
  );
}
