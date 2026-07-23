"use client";

import Link from "next/link";
import { useState } from "react";

import ModelSelect from "@/components/ModelSelect/ModelSelect";
import { useModels } from "@/lib/useModels";

type PredictResult = { label: string; confidence: number };

const RESULT_STYLE: Record<string, { bg: string; text: string; dot: string }> = {
  positive: { bg: "bg-positive-soft", text: "text-positive-strong", dot: "bg-positive" },
  negative: { bg: "bg-negative-soft", text: "text-negative-strong", dot: "bg-negative" },
  neutral: { bg: "bg-neutral-soft", text: "text-secondary", dot: "bg-secondary" },
};

export default function Home() {
  const { models, error: modelsError } = useModels();
  const [selectedModelKey, setSelectedModelKey] = useState("");
  const modelKey = selectedModelKey || models[0]?.key || "";
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
      setError("Could not reach the sentiment API. Is it running on port 8000?");
    } finally {
      setLoading(false);
    }
  }

  const style = result ? RESULT_STYLE[result.label.toLowerCase()] ?? RESULT_STYLE.neutral : null;

  return (
    <div className="flex min-h-screen flex-col items-center bg-bg px-6 py-12">
      <main className="flex w-full max-w-xl flex-col gap-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <span className="flex h-8 w-8 items-center justify-center rounded bg-primary text-sm font-semibold text-white">S</span>
            <div className="flex flex-col leading-tight">
              <span className="text-sm font-semibold text-ink">Signal</span>
              <span className="font-mono text-[10px] uppercase tracking-widest text-ink-faint">Sentiment checker</span>
            </div>
          </div>
          <div className="flex gap-4">
            <Link href="/dashboard" className="text-xs font-medium text-secondary transition-colors hover:text-primary">
              Category dashboard
            </Link>
            <Link href="/results" className="text-xs font-medium text-secondary transition-colors hover:text-primary">
              Model results
            </Link>
          </div>
        </div>

        <div className="flex flex-col gap-1">
          <h1 className="text-2xl font-semibold tracking-tight text-ink">Test a review</h1>
          <p className="text-sm text-ink-soft">Paste review text to see how the model classifies it.</p>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-3 rounded border border-line bg-surface p-5">
          <ModelSelect models={models} value={modelKey} onChange={setSelectedModelKey} />
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
      </main>
    </div>
  );
}
