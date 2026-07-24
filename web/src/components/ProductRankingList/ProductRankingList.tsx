export type RankedProduct = {
  name: string;
  avg_rating: number;
  review_count: number;
  pct_negative: number;
};

export type ProductRanking = {
  category: string | null;
  order: "best" | "worst";
  products: RankedProduct[];
};

export default function ProductRankingList({ ranking }: { ranking: ProductRanking }) {
  const label = ranking.order === "worst" ? "Worst-rated" : "Top-rated";

  return (
    <div className="w-full max-w-[80%] overflow-hidden rounded-lg border border-line bg-surface text-xs shadow-sm">
      <div className="border-b border-line bg-neutral-soft px-3 py-2">
        <p className="font-semibold text-ink">
          {label} {ranking.category ? `in ${ranking.category}` : "products"}
        </p>
      </div>
      <ol className="divide-y divide-line">
        {ranking.products.map((product, index) => (
          <li key={product.name} className="flex items-center justify-between gap-3 px-3 py-2">
            <span className="flex items-center gap-2">
              <span className="font-mono text-ink-faint">{index + 1}.</span>
              <span className="text-ink">{product.name}</span>
            </span>
            <span className="flex shrink-0 flex-col items-end text-ink-soft">
              <span className="font-semibold text-ink">{product.avg_rating.toFixed(2)}★</span>
              <span>{product.review_count.toLocaleString()} reviews</span>
            </span>
          </li>
        ))}
        {ranking.products.length === 0 && <li className="px-3 py-2 text-ink-faint">No products matched.</li>}
      </ol>
    </div>
  );
}
