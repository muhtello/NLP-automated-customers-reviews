// Builds an error string that includes the resolved API base URL so deployment
// misconfiguration (missing/wrong NEXT_PUBLIC_API_BASE_URL) is visible in the UI, not just devtools.
// Distinguishes "server responded with an error status" from "no response at all" (network/CORS
// failure) — those have different causes and collapsing them into one message hides which is which.
export function apiErrorMessage(action: string, err?: unknown): string {
  const base = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (!base) {
    return `${action}: NEXT_PUBLIC_API_BASE_URL is not set in this deployment.`;
  }
  if (err instanceof Error && err.message.startsWith("Request failed")) {
    return `${action}: server at ${base} responded with an error (${err.message}).`;
  }
  return `${action}: got no response from ${base}. Check the API is running and its ALLOWED_ORIGINS includes this site.`;
}
