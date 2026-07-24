import { useEffect, useState } from "react";

import { apiErrorMessage } from "@/lib/apiError";

export type CategoryListItem = {
  slug: string;
  category: string;
  total_reviews: number;
  avg_rating: number;
  pct_negative: number;
};

export function useCategories() {
  const [categories, setCategories] = useState<CategoryListItem[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/categories`)
      .then((response) => {
        if (!response.ok) throw new Error(`Request failed: ${response.status}`);
        return response.json();
      })
      .then(setCategories)
      .catch((err) => setError(apiErrorMessage("Could not reach the API", err)));
  }, []);

  return { categories, error };
}
