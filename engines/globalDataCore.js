export async function getGlobalData() {
  try {
    const res = await fetch("/api/live");
    const data = await res.json();

    return {
      markets: data.markets || {},
      signals: data.signals || [],
      driver: data.dominantDriver || null,
      source: "live"
    };
  } catch (e) {
    return {
      markets: {},
      signals: [],
      driver: null,
      source: "fallback"
    };
  }
}
