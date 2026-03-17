import { loadLiveSignals } from "./liveDataEngine.js";

export async function loadExtendedData() {
  const staticFallback = {
    system: {
      name: "ZENTRA",
      mode: "V1",
      status: "operational"
    },

    markets: {
      oil: 82.4,
      gold: 2180.5,
      sp500: 5120.3,
      interestRate: 4.75,
      shipping: 1460
    },

    signals: [
      {
        title: "Energy Pressure",
        severity: "high",
        category: "energy",
        summary: "Energy costs are rising across key regions."
      },
      {
        title: "Logistics Stress",
        severity: "medium",
        category: "logistics",
        summary: "Shipping routes remain under pressure."
      },
      {
        title: "Market Stress",
        severity: "low",
        category: "markets",
        summary: "Market volatility is present but contained."
      }
    ],

    finance: {
      liquidityPressure: "medium",
      ratePressure: "high",
      volatility: "medium"
    },

    trade: {
      routeStress: "medium",
      customsPressure: "low",
      supplyPressure: "medium"
    },

    dominantDriver: "Energy Pressure",
    source: "static-fallback",
    updatedAt: null
  };

  try {
    const liveFeed = await loadLiveSignals();

    if (!liveFeed) {
      return staticFallback;
    }

    return normalizeData(liveFeed, staticFallback);
  } catch (error) {
    console.error("ZENTRA Data Engine fallback:", error);
    return staticFallback;
  }
}

function normalizeData(liveData, fallback) {
  const markets = {
    oil: numberOrFallback(liveData?.markets?.oil, fallback.markets.oil),
    gold: numberOrFallback(liveData?.markets?.gold, fallback.markets.gold),
    sp500: numberOrFallback(liveData?.markets?.sp500, fallback.markets.sp500),
    interestRate: numberOrFallback(
      liveData?.markets?.interestRate,
      fallback.markets.interestRate
    ),
    shipping: numberOrFallback(
      liveData?.markets?.shipping,
      fallback.markets.shipping
    )
  };

  const signals = Array.isArray(liveData?.signals) && liveData.signals.length
    ? liveData.signals.map((signal) => ({
        title: signal?.title || "Unknown Signal",
        severity: signal?.severity || "low",
        category: signal?.category || "general",
        summary: signal?.summary || "No summary available."
      }))
    : fallback.signals;

  const driver =
    liveData?.dominantDriver ||
    liveData?.driver ||
    fallback.dominantDriver;

  return {
    system: {
      name: liveData?.system?.name || fallback.system.name,
      mode: liveData?.system?.mode || fallback.system.mode,
      status: liveData?.system?.status || fallback.system.status
    },

    markets,
    signals,

    finance: buildFinance(markets),
    trade: buildTrade(markets),

    dominantDriver: driver,
    source: liveData?.source || "live-feed",
    updatedAt: liveData?.updatedAt || null
  };
}

function buildFinance(markets) {
  let liquidityPressure = "low";
  let ratePressure = "low";
  let volatility = "low";

  if (markets.interestRate >= 4.5) {
    ratePressure = "high";
  } else if (markets.interestRate >= 3.5) {
    ratePressure = "medium";
  }

  if (markets.sp500 < 5200) {
    volatility = "medium";
  }
  if (markets.sp500 < 5000) {
    volatility = "high";
  }

  if (markets.gold > 2100) {
    liquidityPressure = "medium";
  }
  if (markets.gold > 2250) {
    liquidityPressure = "high";
  }

  return {
    liquidityPressure,
    ratePressure,
    volatility
  };
}

function buildTrade(markets) {
  let routeStress = "low";
  let customsPressure = "low";
  let supplyPressure = "low";

  if (markets.shipping >= 1200) {
    routeStress = "medium";
    supplyPressure = "medium";
  }

  if (markets.shipping >= 1700) {
    routeStress = "high";
    supplyPressure = "high";
  }

  if (markets.oil >= 80) {
    customsPressure = "low";
  }

  if (markets.oil >= 95) {
    customsPressure = "medium";
  }

  return {
    routeStress,
    customsPressure,
    supplyPressure
  };
}

function numberOrFallback(value, fallback) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}
