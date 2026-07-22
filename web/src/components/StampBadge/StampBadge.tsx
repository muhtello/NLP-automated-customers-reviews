type Verdict = "APPROVED" | "MIXED" | "CAUTION";

function verdictFor(avgRating: number, pctNegative: number): Verdict {
  if (pctNegative >= 0.08 || avgRating < 4.3) return "CAUTION";
  if (pctNegative >= 0.04) return "MIXED";
  return "APPROVED";
}

const VERDICT_COLOR: Record<Verdict, string> = {
  APPROVED: "border-stamp-green text-stamp-green",
  MIXED: "border-stamp-amber text-stamp-amber",
  CAUTION: "border-stamp-red text-stamp-red",
};

export default function StampBadge({
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
  const dims = size === "lg" ? "h-32 w-32" : size === "sm" ? "h-16 w-16" : "h-24 w-24";
  const textSize = size === "lg" ? "text-lg" : size === "sm" ? "text-[10px]" : "text-xs";
  const ratingSize = size === "lg" ? "text-3xl" : size === "sm" ? "text-lg" : "text-2xl";

  return (
    <div
      className={`relative flex ${dims} shrink-0 rotate-[-8deg] flex-col items-center justify-center gap-0.5 rounded-full border-2 border-dashed ${VERDICT_COLOR[verdict]} ${animate ? "animate-stamp-down" : ""}`}
    >
      <div className={`absolute inset-1 rounded-full border ${VERDICT_COLOR[verdict]} opacity-60`} />
      <span className={`font-display font-semibold tracking-wide ${textSize}`}>{verdict}</span>
      <span className={`font-display font-bold ${ratingSize}`}>{avgRating.toFixed(1)}</span>
      <span className={`font-display uppercase tracking-widest ${size === "sm" ? "text-[8px]" : "text-[9px]"} opacity-80`}>
        avg rating
      </span>
    </div>
  );
}
