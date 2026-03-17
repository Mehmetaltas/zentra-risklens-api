export async function getGlobalData() {
  try {

    // 🔴 1. API ÇEK
    const res = await fetch("/api/live"); // vercel api
    const data = await res.json();

    if (!data || !data.markets) {
      throw new Error("API data invalid");
    }

    // 🟢 2. NORMALIZE
    return {
      markets: {
        oil: Number(data.markets.oil),
        gold: Number(data.markets.gold),
        sp500: Number(data.markets.sp500),
        interestRate: Number(data.markets.interestRate),
        shipping: Number(data.markets.shipping)
      },

      signals: data.signals || [],

      macro: {
        inflation: data.inflation || null,
        gdp: data.gdp || null
      },

      source: "live-data-core",
      updatedAt: data.updatedAt || new Date().toISOString()
    };

  } catch (e) {

    console.warn("GLOBAL DATA CORE FALLBACK");

    // 🔁 FALLBACK
    return {
      markets: {
        oil: 82.4,
        gold: 2180.5,
        sp500: 5120.3,
        interestRate: 4.75,
        shipping: 1460
      },

      signals: [
        { title: "Energy Pressure", severity: "high" },
        { title: "Logistics Stress", severity: "medium" }
      ],

      macro: {
        inflation: null,
        gdp: null
      },

      source: "data-core-fallback",
      updatedAt: new Date().toISOString()
    };
  }
}
