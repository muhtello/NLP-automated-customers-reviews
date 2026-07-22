import { useEffect, useState } from "react";

export type CategoryListItem = { slug: string; category: string };

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
      .catch(() => setError("Could not reach the API. Is it running on port 8000?"));
  }, []);

  return { categories, error };
}
