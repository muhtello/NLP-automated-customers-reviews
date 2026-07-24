"use client";

import { useState } from "react";

import { apiErrorMessage } from "@/lib/apiError";
import { useModels } from "@/lib/useModels";

type PredictResult = { label: string; confidence: number };

const RESULT_STYLE: Record<string, { bg: string; text: string; dot: string }> = {
  positive: { bg: "bg-positive-soft", text: "text-positive-strong", dot: "bg-positive" },
  negative: { bg: "bg-negative-soft", text: "text-negative-strong", dot: "bg-negative" },
  neutral: { bg: "bg-neutral-soft", text: "text-secondary", dot: "bg-secondary" },
};

export default function SentimentForm() {
  const { models, error: modelsError } = useModels();
  const modelKey = models[0]?.key || "";
  const [text, setText] = useState("");
  const [result, setResult] = useState<PredictResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: React.SyntheticEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, model: modelKey }),
      });
      if (!response.ok) throw new Error(`Request failed: ${response.status}`);
      setResult(await response.json());
    } catch {
      setError(apiErrorMessage("Could not reach the sentiment API"));
    } finally {
      setLoading(false);
    }
  }

  const style = result ? RESULT_STYLE[result.label.toLowerCase()] ?? RESULT_STYLE.neutral : null;

  return (
    <div className="flex flex-col gap-3 rounded-xl border border-line bg-surface p-5">
      <div className="flex flex-col gap-1">
        <h2 className="text-base font-semibold text-ink">Test a review</h2>
        <p className="text-sm text-ink-soft">Paste review text to see how the model classifies it.</p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <textarea
          value={text}
          onChange={(event) => setText(event.target.value)}
          placeholder="Paste a product review..."
          rows={5}
          className="rounded border border-line p-3 text-sm text-ink outline-none transition-colors placeholder:text-ink-faint focus:border-2 focus:border-primary"
        />
        <button
          type="submit"
          disabled={loading || text.trim() === "" || modelKey === ""}
          className="rounded bg-primary-strong px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-primary disabled:cursor-not-allowed disabled:bg-ink-faint"
        >
          {loading ? "Predicting..." : "Predict sentiment"}
        </button>
      </form>

      {result && style && (
        <div className={`flex items-center gap-2 rounded-badge ${style.bg} px-4 py-3`}>
          <span className={`h-2 w-2 rounded-full ${style.dot}`} />
          <p className={`text-sm font-medium ${style.text}`}>
            {result.label} &middot; {(result.confidence * 100).toFixed(1)}% confidence
          </p>
        </div>
      )}
      {(error || modelsError) && <p className="text-sm text-negative-strong">{error || modelsError}</p>}
    </div>
  );
}
