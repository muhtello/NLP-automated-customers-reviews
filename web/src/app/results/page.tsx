"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import ModelSelect from "@/components/ModelSelect/ModelSelect";
import { useModels } from "@/lib/useModels";

type ClassMetrics = { precision: number; recall: number; "f1-score": number; support: number };

type SentimentMetrics = {
  accuracy: number;
  negative: ClassMetrics;
  positive: ClassMetrics;
  macro_avg: ClassMetrics;
  confusion_matrix_url: string;
};

function pct(value: number): string {
  return `${(value * 100).toFixed(1)}%`;
}

export default function Results() {
  const { models, error: modelsError } = useModels();
  const [selectedModelKey, setSelectedModelKey] = useState("");
  const modelKey = selectedModelKey || models[0]?.key || "";
  const [metrics, setMetrics] = useState<SentimentMetrics | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (modelKey === "") return;
    fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/metrics/sentiment?model=${modelKey}`)
      .then((response) => {
        if (!response.ok) throw new Error(`Request failed: ${response.status}`);
        return response.json();
      })
      .then((data) => {
        setMetrics(data);
        setError("");
      })
      .catch(() => {
        setError("Could not reach the sentiment API. Is it running on port 8000?");
        setMetrics(null);
      });
  }, [modelKey]);

  const rows: [string, ClassMetrics][] = metrics
    ? [
        ["Negative", metrics.negative],
        ["Positive", metrics.positive],
        ["Macro avg", metrics.macro_avg],
      ]
    : [];

  return (
    <div className="min-h-screen bg-bg">
      <header className="border-b border-line bg-surface px-6 py-4">
        <div className="mx-auto flex max-w-2xl items-center justify-between">
          <Link href="/" className="text-xs font-medium text-secondary transition-colors hover:text-primary">
            &larr; Sentiment checker
          </Link>
        </div>
      </header>

      <main className="mx-auto flex max-w-2xl flex-col gap-6 px-6 py-8">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-semibold tracking-tight text-ink">Model results</h1>
          <ModelSelect models={models} value={modelKey} onChange={setSelectedModelKey} />
        </div>

        {(error || modelsError) && <p className="text-sm text-negative-strong">{error || modelsError}</p>}
        {!metrics && !error && !modelsError && <p className="font-mono text-xs uppercase tracking-widest text-ink-faint">Loading...</p>}

        {metrics && (
          <>
            <div className="rounded border border-line bg-surface p-5">
              <p className="text-xs uppercase tracking-widest text-ink-faint">Overall accuracy</p>
              <p className="font-mono text-3xl font-semibold text-primary">{pct(metrics.accuracy)}</p>
              <p className="mt-1 text-sm text-ink-soft">on the held-out test set</p>
            </div>

            <div className="overflow-hidden rounded border border-line bg-surface">
              <table className="w-full border-collapse text-left text-sm">
                <thead>
                  <tr className="border-b border-line bg-surface-sunken">
                    <th className="px-4 py-2.5 font-medium text-ink-soft">Class</th>
                    <th className="px-4 py-2.5 font-medium text-ink-soft">Precision</th>
                    <th className="px-4 py-2.5 font-medium text-ink-soft">Recall</th>
                    <th className="px-4 py-2.5 font-medium text-ink-soft">F1-score</th>
                    <th className="px-4 py-2.5 font-medium text-ink-soft">Support</th>
                  </tr>
                </thead>
                <tbody className="font-mono">
                  {rows.map(([name, row]) => (
                    <tr key={name} className="border-b border-line last:border-none">
                      <td className="px-4 py-2.5 font-sans font-medium text-ink">{name}</td>
                      <td className="px-4 py-2.5 text-ink-soft">{pct(row.precision)}</td>
                      <td className="px-4 py-2.5 text-ink-soft">{pct(row.recall)}</td>
                      <td className="px-4 py-2.5 text-ink-soft">{pct(row["f1-score"])}</td>
                      <td className="px-4 py-2.5 text-ink-soft">{row.support}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div>
              <h2 className="mb-2 text-sm font-semibold uppercase tracking-widest text-ink-soft">Confusion matrix</h2>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={`${process.env.NEXT_PUBLIC_API_BASE_URL}${metrics.confusion_matrix_url}`}
                alt="Confusion matrix"
                className="max-w-full rounded border border-line"
              />
            </div>
          </>
        )}
      </main>
    </div>
  );
}
