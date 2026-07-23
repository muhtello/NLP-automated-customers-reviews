export type ProductComparison = {
  name: string;
  review_count: number;
  avg_rating: number;
  best_review: { rating: number; text: string };
  worst_review: { rating: number; text: string };
};

export default function ProductComparisonTable({ comparison }: { comparison: ProductComparison }) {
  return (
    <div className="w-full max-w-[80%] overflow-hidden rounded-lg border border-line bg-surface text-xs shadow-sm">
      <div className="border-b border-line bg-neutral-soft px-3 py-2">
        <p className="font-semibold text-ink">{comparison.name}</p>
        <p className="text-ink-faint">
          {comparison.avg_rating.toFixed(2)} avg &middot; {comparison.review_count.toLocaleString()} reviews
        </p>
      </div>
      <div className="grid grid-cols-2 divide-x divide-line">
        <div className="flex flex-col gap-1 p-3">
          <p className="font-semibold text-positive-strong">Best review &middot; {comparison.best_review.rating}★</p>
          <p className="text-ink-soft">{comparison.best_review.text}</p>
        </div>
        <div className="flex flex-col gap-1 p-3">
          <p className="font-semibold text-negative-strong">Worst review &middot; {comparison.worst_review.rating}★</p>
          <p className="text-ink-soft">{comparison.worst_review.text}</p>
        </div>
      </div>
    </div>
  );
}
