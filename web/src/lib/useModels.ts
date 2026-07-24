import { useEffect, useState } from "react";

import { apiErrorMessage } from "@/lib/apiError";

export type ModelInfo = { key: string; display_name: string };

export function useModels() {
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/models`)
      .then((response) => {
        if (!response.ok) throw new Error(`Request failed: ${response.status}`);
        return response.json();
      })
      .then(setModels)
      .catch(() => setError(apiErrorMessage("Could not reach the sentiment API")));
  }, []);

  return { models, error };
}
