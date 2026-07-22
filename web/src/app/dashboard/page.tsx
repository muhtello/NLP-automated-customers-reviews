"use client";

import Link from "next/link";

import { useCategories } from "@/lib/useCategories";

export default function Dashboard() {
  const { categories, error } = useCategories();

  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-6 p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Product Category Dashboard</h1>
        <Link href="/" className="text-sm text-blue-600 hover:underline">
          Sentiment checker
        </Link>
      </div>

      {error && <p className="text-red-600">{error}</p>}
      {!error && categories.length === 0 && <p>Loading...</p>}

      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        {categories.map((item) => (
          <Link
            key={item.slug}
            href={`/dashboard/${item.slug}`}
            className="rounded border border-gray-300 p-4 hover:border-blue-500 hover:bg-blue-50"
          >
            <h2 className="font-medium">{item.category}</h2>
            <p className="text-sm text-gray-500">View recommendation article</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
