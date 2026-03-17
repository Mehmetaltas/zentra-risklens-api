export async function loadLiveSignals() {
  try {
    const response = await fetch("https://zentra-live-api.vercel.app/api/live", {
      cache: "no-store"
    });

    if (!response.ok) {
      console.error("API response not OK:", response.status);
      return null;
    }

    const data = await response.json();

    return normalizeLivePayload(data, "vercel-live-api");
  } catch (error) {
    console.error("Live feed error:", error);
    return null;
  }
}

function normalizeLivePayload(data, source) {
  return {
    system: {
      name: data?.system?.name || "ZENTRA",
      mode: data?.system?.mode || "LIVE",
      status: data?.system?.status || "operational"
    },

    markets: {
      oil: numberOrNull(data?.markets?.oil),
      gold: numberOrNull(data?.markets?.gold),
      sp500: numberOrNull(data?.markets?.sp500),
      interestRate: numberOrNull(data?.markets?.interestRate),
      shipping: numberOrNull(data?.markets?.shipping)
    },

    signals: Array.isArray(data?.signals)
      ? data.signals.map((signal) => ({
          title: signal?.title || "Unknown Signal",
          severity: signal?.severity || "low",
          category: signal?.category || "general",
          summary: signal?.summary || "No summary available."
        }))
      : [],

    dominantDriver: data?.dominantDriver || "Unknown",
    source,
    updated
