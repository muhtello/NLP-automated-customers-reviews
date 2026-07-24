import { useEffect, useState } from "react";

import { apiErrorMessage } from "@/lib/apiError";

export type ProductListItem = { name: string; review_count: number; avg_rating: number };

export function useProductSearch(query: string) {
  const [products, setProducts] = useState<ProductListItem[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const controller = new AbortController();
    fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/products?q=${encodeURIComponent(query)}`, {
      signal: controller.signal,
    })
      .then((response) => {
        if (!response.ok) throw new Error(`Request failed: ${response.status}`);
        return response.json();
      })
      .then((data) => {
        setProducts(data);
        setError("");
      })
      .catch((err) => {
        if (err.name === "AbortError") return;
        setError(apiErrorMessage("Could not reach the API", err));
      });

    return () => controller.abort();
  }, [query]);

  return { products, error };
}
