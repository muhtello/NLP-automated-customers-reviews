"use client";

import Link from "next/link";

import { useCategories } from "@/lib/useCategories";

const MIN_SIZE = 110;
const MAX_SIZE = 240;

function verdictColor(pctNegative: number): { bg: string; border: string; text: string } {
  if (pctNegative >= 0.08) return { bg: "bg-negative-soft", border: "border-negative/40", text: "text-negative-strong" };
  if (pctNegative >= 0.04) return { bg: "bg-neutral-soft", border: "border-secondary/30", text: "text-secondary" };
  return { bg: "bg-positive-soft", border: "border-positive/40", text: "text-positive-strong" };
}

export default function Clustering() {
  const { categories, error } = useCategories();

  if (error) {
    return <p className="rounded border border-dashed border-negative bg-negative-soft p-4 text-sm text-negative-strong">{error}</p>;
  }
  if (categories.length === 0) {
    return <p className="font-mono text-xs uppercase tracking-widest text-ink-faint">Loading clusters...</p>;
  }

  const counts = categories.map((item) => item.total_reviews);
  const min = Math.min(...counts);
  const max = Math.max(...counts);

  function sizeFor(count: number): number {
    if (max === min) return (MIN_SIZE + MAX_SIZE) / 2;
    const ratio = Math.sqrt((count - min) / (max - min));
    return MIN_SIZE + ratio * (MAX_SIZE - MIN_SIZE);
  }

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h2 className="text-lg font-semibold tracking-tight text-ink">NLP-mapped meta-categories</h2>
        <p className="text-sm text-ink-soft">Bubble size reflects review volume; color reflects negative-sentiment rate.</p>
      </div>

      <div className="flex min-h-[420px] flex-wrap items-center justify-center gap-6 rounded-xl border border-line bg-surface p-10">
        {categories.map((item) => {
          const size = sizeFor(item.total_reviews);
          const style = verdictColor(item.pct_negative);
          return (
            <Link
              key={item.slug}
              href={`/dashboard/${item.slug}`}
              style={{ width: size, height: size }}
              className={`flex flex-col items-center justify-center rounded-full border p-3 text-center transition-transform hover:scale-105 ${style.bg} ${style.border}`}
            >
              <span className={`text-sm font-semibold leading-tight ${style.text}`}>{item.category}</span>
              <span className="mt-1 font-mono text-xs text-ink-faint">{item.total_reviews.toLocaleString()} reviews</span>
            </Link>
          );
        })}
      </div>

      <div className="flex flex-col gap-3 rounded-xl border border-line bg-surface p-5">
        <h3 className="text-sm font-semibold uppercase tracking-widest text-ink-soft">Cluster detail</h3>
        <div className="divide-y divide-line">
          {categories.map((item) => (
            <div key={item.slug} className="flex items-center justify-between py-3">
              <Link href={`/dashboard/${item.slug}`} className="text-sm font-medium text-primary hover:underline">
                {item.category}
              </Link>
              <div className="flex items-center gap-6 font-mono text-xs text-ink-soft">
                <span>{item.total_reviews.toLocaleString()} reviews</span>
                <span>{item.avg_rating.toFixed(2)} avg rating</span>
                <span className="text-negative-strong">{(item.pct_negative * 100).toFixed(1)}% negative</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
