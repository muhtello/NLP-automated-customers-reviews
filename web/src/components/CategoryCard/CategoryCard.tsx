import Link from "next/link";

import CategoryIcon from "@/components/CategoryIcon/CategoryIcon";
import StampBadge from "@/components/StampBadge/StampBadge";
import type { CategoryListItem } from "@/lib/useCategories";

export default function CategoryCard({ item, shareOfTotal }: { item: CategoryListItem; shareOfTotal: number }) {
  return (
    <Link
      href={`/dashboard/${item.slug}`}
      className="group flex flex-col gap-4 rounded-sm border border-line bg-paper-raised p-5 transition-all hover:-translate-y-0.5 hover:border-ledger hover:shadow-[4px_4px_0_0_var(--color-ledger)]"
    >
      <div className="flex items-start justify-between">
        <div className="flex flex-col gap-1">
          <span className="font-display text-[11px] font-medium uppercase tracking-widest text-ink-soft">
            {shareOfTotal.toFixed(0)}% of all reviews
          </span>
          <h2 className="font-display text-lg font-semibold leading-snug text-ink">{item.category}</h2>
        </div>
        <CategoryIcon slug={item.slug} className="mt-1 h-6 w-6 shrink-0 text-ledger-soft" />
      </div>

      <div className="flex items-end justify-between border-t border-dashed border-line pt-3">
        <dl className="flex flex-col gap-1 font-display text-xs text-ink-soft">
          <div>
            <dt className="inline uppercase tracking-wide">Reviews on file&nbsp;</dt>
            <dd className="inline font-semibold text-ink">{item.total_reviews.toLocaleString()}</dd>
          </div>
          <div>
            <dt className="inline uppercase tracking-wide">Negative rate&nbsp;</dt>
            <dd className="inline font-semibold text-ink">{(item.pct_negative * 100).toFixed(1)}%</dd>
          </div>
        </dl>
        <StampBadge avgRating={item.avg_rating} pctNegative={item.pct_negative} size="sm" />
      </div>
    </Link>
  );
}
