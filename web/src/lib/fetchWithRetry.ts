// Render's free-tier API spins down when idle; a request that arrives while it's waking
// back up gets a 502 from Render's own edge before the app instance is ready. Retrying a
// couple of times with a short delay rides out that window instead of surfacing an error.
const RETRY_STATUSES = new Set([502, 503, 504]);
const RETRY_DELAYS_MS = [1500, 3000];

function wait(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function fetchWithRetry(input: RequestInfo | URL, init?: RequestInit): Promise<Response> {
  for (let attempt = 0; attempt <= RETRY_DELAYS_MS.length; attempt++) {
    const isLastAttempt = attempt === RETRY_DELAYS_MS.length;
    try {
      const response = await fetch(input, init);
      if (response.ok || !RETRY_STATUSES.has(response.status) || isLastAttempt) {
        return response;
      }
    } catch (err) {
      if (isLastAttempt || (err instanceof Error && err.name === "AbortError")) throw err;
    }
    await wait(RETRY_DELAYS_MS[attempt]);
  }
  throw new Error("unreachable");
}
