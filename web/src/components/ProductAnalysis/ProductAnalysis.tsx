"use client";

import { useState } from "react";

import ModelSelect from "@/components/ModelSelect/ModelSelect";
import { useModels } from "@/lib/useModels";

type Analysis = {
  name: string;
  model: string;
  review_count: number;
  sample_size: number;
  avg_rating: number;
  positive_count: number;
  negative_count: number;
  pct_positive: number;
  pct_negative: number;
};

export default function ProductAnalysis({ productName }: { productName: string }) {
  const { models, error: modelsError } = useModels();
  const [selectedModelKey, setSelectedModelKey] = useState("");
  const modelKey = selectedModelKey || models[0]?.key || "";
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function runAnalysis() {
    setLoading(true);
    setError("");
    setAnalysis(null);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/products/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: productName, model: modelKey }),
      });
      if (!response.ok) throw new Error(`Request failed: ${response.status}`);
      setAnalysis(await response.json());
    } catch {
      setError("Could not reach the sentiment API. Is it running on port 8000?");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col gap-4 rounded-xl border border-line bg-surface p-5">
      <div className="flex flex-col gap-3">
        <div>
          <p className="text-xs uppercase tracking-widest text-ink-faint">Selected product</p>
          <h2 className="text-base font-semibold text-ink">{productName}</h2>
        </div>
        <ModelSelect models={models} value={modelKey} onChange={setSelectedModelKey} />
      </div>

      <button
        onClick={runAnalysis}
        disabled={loading || modelKey === ""}
        className="rounded bg-primary-strong px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-primary disabled:cursor-not-allowed disabled:bg-ink-faint"
      >
        {loading ? "Running model on reviews..." : "Analyze all reviews"}
      </button>

      {(error || modelsError) && <p className="text-sm text-negative-strong">{error || modelsError}</p>}

      {analysis && (
        <div className="flex flex-col gap-4 border-t border-line pt-4">
          <p className="font-mono text-xs uppercase tracking-widest text-ink-faint">
            {analysis.sample_size < analysis.review_count
              ? `Model ran on a random sample of ${analysis.sample_size.toLocaleString()} of ${analysis.review_count.toLocaleString()} reviews`
              : `Model ran on all ${analysis.review_count.toLocaleString()} reviews`}
          </p>

          <div className="flex flex-col gap-2">
            <div className="flex justify-between text-sm">
              <span className="font-medium text-positive-strong">Positive &middot; {analysis.positive_count.toLocaleString()}</span>
              <span className="font-mono text-positive-strong">{(analysis.pct_positive * 100).toFixed(1)}%</span>
            </div>
            <div className="h-3 overflow-hidden rounded-full bg-neutral-soft">
              <div className="h-full bg-positive" style={{ width: `${analysis.pct_positive * 100}%` }} />
            </div>
          </div>

          <div className="flex flex-col gap-2">
            <div className="flex justify-between text-sm">
              <span className="font-medium text-negative-strong">Negative &middot; {analysis.negative_count.toLocaleString()}</span>
              <span className="font-mono text-negative-strong">{(analysis.pct_negative * 100).toFixed(1)}%</span>
            </div>
            <div className="h-3 overflow-hidden rounded-full bg-neutral-soft">
              <div className="h-full bg-negative" style={{ width: `${analysis.pct_negative * 100}%` }} />
            </div>
          </div>

          <p className="text-xs text-ink-soft">
            Star-rating average on file: <span className="font-mono font-semibold text-ink">{analysis.avg_rating.toFixed(2)}</span>
          </p>
        </div>
      )}
    </div>
  );
}
