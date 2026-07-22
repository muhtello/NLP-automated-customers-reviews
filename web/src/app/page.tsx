"use client";

import Link from "next/link";
import { useState } from "react";

import ModelSelect from "@/components/ModelSelect/ModelSelect";
import { useModels } from "@/lib/useModels";

type PredictResult = { label: string; confidence: number };

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

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-6">
      <main className="flex w-full max-w-xl flex-col gap-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-semibold">Review Sentiment Checker</h1>
          <div className="flex gap-4">
            <Link href="/dashboard" className="text-sm text-blue-600 hover:underline">
              Category dashboard
            </Link>
            <Link href="/results" className="text-sm text-blue-600 hover:underline">
              View model results
            </Link>
          </div>
        </div>
        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <ModelSelect models={models} value={modelKey} onChange={setSelectedModelKey} />
          <textarea
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder="Paste a product review..."
            rows={5}
            className="rounded border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={loading || text.trim() === "" || modelKey === ""}
            className="rounded bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-gray-400"
          >
            {loading ? "Predicting..." : "Predict sentiment"}
          </button>
        </form>
        {result && (
          <p>
            Prediction: <strong>{result.label}</strong> ({(result.confidence * 100).toFixed(1)}% confidence)
          </p>
        )}
        {(error || modelsError) && <p className="text-red-600">{error || modelsError}</p>}
      </main>
    </div>
  );
}
