import Link from "next/link";

import CategoryIcon from "@/components/CategoryIcon/CategoryIcon";
import VerdictBadge from "@/components/VerdictBadge/VerdictBadge";
import type { CategoryListItem } from "@/lib/useCategories";

export default function CategoryCard({ item, shareOfTotal }: { item: CategoryListItem; shareOfTotal: number }) {
  return (
    <Link
      href={`/dashboard/${item.slug}`}
      className="group flex flex-col gap-4 rounded border border-line bg-surface p-5 transition-all hover:-translate-y-0.5 hover:border-primary/30 hover:shadow-[0_8px_24px_-4px_rgb(46_58_140_/_0.15)]"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex flex-col gap-1">
          <span className="font-mono text-[11px] font-medium uppercase tracking-widest text-ink-faint">
            {shareOfTotal.toFixed(0)}% of all reviews
          </span>
          <h2 className="text-lg font-semibold leading-snug tracking-tight text-ink">{item.category}</h2>
        </div>
        <span className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded bg-primary-soft text-primary">
          <CategoryIcon slug={item.slug} className="h-5 w-5" />
        </span>
      </div>

      <div className="flex items-end justify-between border-t border-line pt-3">
        <dl className="flex flex-col gap-1 text-xs text-ink-soft">
          <div>
            <dt className="inline">Reviews on file&nbsp;</dt>
            <dd className="inline font-mono font-semibold text-ink">{item.total_reviews.toLocaleString()}</dd>
          </div>
          <div>
            <dt className="inline">Negative rate&nbsp;</dt>
            <dd className="inline font-mono font-semibold text-ink">{(item.pct_negative * 100).toFixed(1)}%</dd>
          </div>
        </dl>
        <VerdictBadge avgRating={item.avg_rating} pctNegative={item.pct_negative} size="sm" />
      </div>
    </Link>
  );
}
