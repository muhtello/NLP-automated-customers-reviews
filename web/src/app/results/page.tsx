"use client";

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
    <div className="mx-auto flex max-w-2xl flex-col gap-6 p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Sentiment Model Results</h1>
        <ModelSelect models={models} value={modelKey} onChange={setSelectedModelKey} />
      </div>

      {(error || modelsError) && <p className="text-red-600">{error || modelsError}</p>}
      {!metrics && !error && !modelsError && <p>Loading...</p>}

      {metrics && (
        <>
          <p>
            Overall accuracy: <strong>{pct(metrics.accuracy)}</strong> on the held-out test set.
          </p>

          <table className="w-full border-collapse text-left">
            <thead>
              <tr className="border-b border-gray-300">
                <th className="py-2">Class</th>
                <th className="py-2">Precision</th>
                <th className="py-2">Recall</th>
                <th className="py-2">F1-score</th>
                <th className="py-2">Support</th>
              </tr>
            </thead>
            <tbody>
              {rows.map(([name, row]) => (
                <tr key={name} className="border-b border-gray-200">
                  <td className="py-2 font-medium">{name}</td>
                  <td className="py-2">{pct(row.precision)}</td>
                  <td className="py-2">{pct(row.recall)}</td>
                  <td className="py-2">{pct(row["f1-score"])}</td>
                  <td className="py-2">{row.support}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <div>
            <h2 className="mb-2 text-lg font-medium">Confusion Matrix</h2>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={`${process.env.NEXT_PUBLIC_API_BASE_URL}${metrics.confusion_matrix_url}`}
              alt="Confusion matrix"
              className="max-w-full rounded border border-gray-200"
            />
          </div>
        </>
      )}
    </div>
  );
}
