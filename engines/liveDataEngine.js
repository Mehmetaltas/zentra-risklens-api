export async function loadLiveSignals() {
  const localFeed = await tryLocalFeed();
  if (localFeed) return localFeed;

  const marketFeed = await tryMarketFeed();
  if (marketFeed) return marketFeed;

  return null;
}

async function tryLocalFeed() {
  try {
    const response = await fetch("/global-signals.json", {
      cache: "no-store"
    });

    if (!response.ok) return null;

    const data = await response.json();

    return normalizeLivePayload(data, "local-json");
  } catch (error) {
    console.error("Local live feed error:", error);
    return null;
  }
}

async function tryMarketFeed() {
  try {
    const response = await fetch("/api/live-data.json", {
      cache: "no-store"
    });

    if (!response.ok) return null;

    const data = await response.json();

    return normalizeLivePayload(data, "api-live-feed");
  } catch (error) {
    return null;
  }
}

function normalizeLivePayload(data, source) {
  const markets = {
    oil: numberOrNull(data?.markets?.oil),
    gold: numberOrNull(data?.markets?.gold),
    sp500: numberOrNull(data?.markets?.sp500),
    interestRate: numberOrNull(data?.markets?.interestRate),
    shipping: numberOrNull(data?.markets?.shipping)
  };

  const signals = Array.isArray(data?.signals)
    ? data.signals.map((signal) => ({
        title: signal?.title || "Unknown Signal",
        severity: signal?.severity || "low",
        category: signal?.category || "general",
        summary: signal?.summary || "No summary available."
      }))
    : [];

  return {
    system: {
      name: data?.system?.name || "ZENTRA",
      mode: data?.system?.mode || "V1",
      status: data?.system?.status || "operational"
    },
    markets,
    signals,
    dominantDriver: data?.dominantDriver || data?.driver || "Unknown",
    source,
    updatedAt: data?.updatedAt || new Date().toISOString()
  };
}

function numberOrNull(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}
