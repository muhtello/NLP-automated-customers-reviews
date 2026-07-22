"use client";

import Link from "next/link";

import CategoryCard from "@/components/CategoryCard/CategoryCard";
import { useCategories } from "@/lib/useCategories";

export default function Dashboard() {
  const { categories, error } = useCategories();
  const totalReviews = categories.reduce((sum, item) => sum + item.total_reviews, 0);

  return (
    <div className="min-h-screen">
      <header className="border-b border-line bg-ledger px-6 py-5 text-paper">
        <div className="mx-auto flex max-w-4xl items-center justify-between">
          <div className="flex flex-col gap-0.5">
            <span className="font-display text-[11px] uppercase tracking-[0.2em] text-paper/70">Manifest No. 2026-07</span>
            <h1 className="font-display text-xl font-semibold tracking-tight">Review Ledger</h1>
          </div>
          <Link href="/" className="font-display text-xs uppercase tracking-widest text-paper/80 underline-offset-4 hover:text-paper hover:underline">
            Sentiment Desk &rarr;
          </Link>
        </div>
      </header>

      <main className="mx-auto flex max-w-4xl flex-col gap-6 p-6">
        <p className="font-display text-xs uppercase tracking-widest text-ink-soft">
          {error
            ? "Ledger unreachable"
            : categories.length === 0
              ? "Loading manifest..."
              : `${totalReviews.toLocaleString()} reviews classified · ${categories.length} categories on file`}
        </p>

        {error && (
          <p className="rounded-sm border border-dashed border-stamp-red bg-paper-raised p-4 text-sm text-stamp-red">
            {error} Start it with <code className="font-display">uvicorn src.main:app --reload</code> from the{" "}
            <code className="font-display">api/</code> directory.
          </p>
        )}

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
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
