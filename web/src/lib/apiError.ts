// Builds an error string that includes the resolved API base URL so deployment
// misconfiguration (missing/wrong NEXT_PUBLIC_API_BASE_URL) is visible in the UI, not just devtools.
export function apiErrorMessage(action: string): string {
  const base = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (!base) {
    return `${action}: NEXT_PUBLIC_API_BASE_URL is not set in this deployment.`;
  }
  return `${action}: tried ${base}. Check the API is running and its ALLOWED_ORIGINS includes this site.`;
}
