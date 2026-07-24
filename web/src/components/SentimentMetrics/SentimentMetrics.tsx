"use client";

import { useEffect, useState } from "react";

import { useModels } from "@/lib/useModels";

type ClassMetrics = { precision: number; recall: number; "f1-score": number; support: number };

type SentimentMetricsData = {
  accuracy: number;
  negative: ClassMetrics;
  positive: ClassMetrics;
  macro_avg: ClassMetrics;
  confusion_matrix_url: string;
};

function pct(value: number): string {
  return `${(value * 100).toFixed(1)}%`;
}

export default function SentimentMetrics() {
  const { models, error: modelsError } = useModels();
  const modelKey = models[0]?.key || "";
  const [metrics, setMetrics] = useState<SentimentMetricsData | null>(null);
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
    <div className="flex flex-col gap-4 rounded-xl border border-line bg-surface p-5">
      <h2 className="text-base font-semibold text-ink">Model results</h2>

      {(error || modelsError) && <p className="text-sm text-negative-strong">{error || modelsError}</p>}
      {!metrics && !error && !modelsError && <p className="font-mono text-xs uppercase tracking-widest text-ink-faint">Loading...</p>}

      {metrics && (
        <>
          <div className="rounded-lg border border-line bg-surface-sunken p-4">
            <p className="text-xs uppercase tracking-widest text-ink-faint">Overall accuracy</p>
            <p className="font-mono text-3xl font-semibold text-primary">{pct(metrics.accuracy)}</p>
            <p className="mt-1 text-sm text-ink-soft">on the held-out test set</p>
          </div>

          <div className="overflow-hidden rounded-lg border border-line">
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
            <h3 className="mb-2 text-sm font-semibold uppercase tracking-widest text-ink-soft">Confusion matrix</h3>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={`${process.env.NEXT_PUBLIC_API_BASE_URL}${metrics.confusion_matrix_url}`}
              alt="Confusion matrix"
              className="max-w-full rounded border border-line"
            />
          </div>
        </>
      )}
    </div>
  );
}
