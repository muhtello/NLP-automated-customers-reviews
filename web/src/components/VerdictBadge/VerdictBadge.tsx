type Verdict = "POSITIVE" | "MIXED" | "NEGATIVE";

function verdictFor(avgRating: number, pctNegative: number): Verdict {
  if (pctNegative >= 0.08 || avgRating < 4.3) return "NEGATIVE";
  if (pctNegative >= 0.04) return "MIXED";
  return "POSITIVE";
}

const VERDICT_STYLE: Record<Verdict, { ring: string; text: string; dot: string }> = {
  POSITIVE: { ring: "ring-positive/25", text: "text-positive-strong", dot: "bg-positive" },
  MIXED: { ring: "ring-secondary/20", text: "text-secondary", dot: "bg-secondary" },
  NEGATIVE: { ring: "ring-negative/25", text: "text-negative-strong", dot: "bg-negative" },
};

const VERDICT_BG: Record<Verdict, string> = {
  POSITIVE: "bg-positive-soft",
  MIXED: "bg-neutral-soft",
  NEGATIVE: "bg-negative-soft",
};

export default function VerdictBadge({
  avgRating,
  pctNegative,
  size = "md",
  animate = false,
}: {
  avgRating: number;
  pctNegative: number;
  size?: "sm" | "md" | "lg";
  animate?: boolean;
}) {
  const verdict = verdictFor(avgRating, pctNegative);
  const style = VERDICT_STYLE[verdict];
  const pad = size === "lg" ? "px-4 py-2.5" : size === "sm" ? "px-2.5 py-1" : "px-3 py-1.5";
  const labelSize = size === "lg" ? "text-xs" : "text-[10px]";
  const ratingSize = size === "lg" ? "text-2xl" : size === "sm" ? "text-sm" : "text-base";

  return (
    <div
      className={`flex shrink-0 flex-col items-start gap-1 rounded-badge ${VERDICT_BG[verdict]} ring-1 ${style.ring} ${pad} ${animate ? "animate-fade-up" : ""}`}
    >
      <span className={`flex items-center gap-1.5 font-display ${labelSize} font-semibold uppercase tracking-widest ${style.text}`}>
        <span className={`h-1.5 w-1.5 rounded-full ${style.dot}`} />
        {verdict}
      </span>
      <span className={`font-mono font-semibold text-ink ${ratingSize}`}>
        {avgRating.toFixed(1)} <span className="text-ink-faint font-normal text-[10px] uppercase tracking-wide">avg</span>
      </span>
    </div>
  );
}
