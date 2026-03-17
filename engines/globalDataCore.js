export async function getGlobalData() {
  const sources = await Promise.allSettled([
    fetchFromLiveApi(),
    fetchFromFredProxy(),
    fetchFromWorldBankProxy(),
    fetchFromCommodityProxy()
  ]);

  const live = pickValue(sources, 0);
  const fred = pickValue(sources, 1);
  const worldBank = pickValue(sources, 2);
  const commodity = pickValue(sources, 3);

  const merged = mergeGlobalData({
    live,
    fred,
    worldBank,
    commodity
  });

  return merged;
}

async function fetchFromLiveApi() {
  const response = await fetch("https://zentra-live-api.vercel.app/api/live", {
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`live api ${response.status}`);
  }

  const data = await response.json();

  return {
    markets: {
      oil: toNumberOrNull(data?.markets?.oil),
      gold: toNumberOrNull(data?.markets?.gold),
      sp500: toNumberOrNull(data?.markets?.sp500),
      interestRate: toNumberOrNull(data?.markets?.interestRate),
      shipping: toNumberOrNull(data?.markets?.shipping)
    },
    signals: Array.isArray(data?.signals) ? data.signals : [],
    source: "live-api",
    updatedAt: data?.updatedAt || new Date().toISOString()
  };
}

async function fetchFromFredProxy() {
  const response = await fetch("https://zentra-live-api.vercel.app/api/fred", {
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`fred api ${response.status}`);
  }

  const data = await response.json();

  return {
    macro: {
      inflation: toNumberOrNull(data?.inflation),
      interestRate: toNumberOrNull(data?.interestRate),
      unemployment: toNumberOrNull(data?.unemployment)
    },
    source: "fred",
    updatedAt: data?.updatedAt || new Date().toISOString()
  };
}

async function fetchFromWorldBankProxy() {
  const response = await fetch("https://zentra-live-api.vercel.app/api/worldbank", {
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`worldbank api ${response.status}`);
  }

  const data = await response.json();

  return {
    macro: {
      gdp: toNumberOrNull(data?.gdp),
      population: toNumberOrNull(data?.population),
      tradePercentGdp: toNumberOrNull(data?.tradePercentGdp)
    },
    source: "worldbank",
    updatedAt: data?.updatedAt || new Date().toISOString()
  };
}

async function fetchFromCommodityProxy() {
  const response = await fetch("https://zentra-live-api.vercel.app/api/commodities", {
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`commodity api ${response.status}`);
  }

  const data = await response.json();

  return {
    markets: {
      oil: toNumberOrNull(data?.oil),
      gold: toNumberOrNull(data?.gold),
      copper: toNumberOrNull(data?.copper),
      wheat: toNumberOrNull(data?.wheat)
    },
    source: "commodities",
    updatedAt: data?.updatedAt || new Date().toISOString()
  };
}

function mergeGlobalData({ live, fred, worldBank, commodity }) {
  const fallback = getFallbackData();

  const markets = {
    oil:
      firstNumber(
        live?.markets?.oil,
        commodity?.markets?.oil,
        fallback.markets.oil
      ),
    gold:
      firstNumber(
        live?.markets?.gold,
        commodity?.markets?.gold,
        fallback.markets.gold
      ),
    sp500:
      firstNumber(
        live?.markets?.sp500,
        fallback.markets.sp500
      ),
    interestRate:
      firstNumber(
        fred?.macro?.interestRate,
        live?.markets?.interestRate,
        fallback.markets.interestRate
      ),
    shipping:
      firstNumber(
        live?.markets?.shipping,
        fallback.markets.shipping
      ),
    copper:
      firstNumber(
        commodity?.markets?.copper,
        fallback.markets.copper
      ),
    wheat:
      firstNumber(
        commodity?.markets?.wheat,
        fallback.markets.wheat
      )
  };

  const macro = {
    inflation:
      firstNumber(
        fred?.macro?.inflation,
        fallback.macro.inflation
      ),
    gdp:
      firstNumber(
        worldBank?.macro?.gdp,
        fallback.macro.gdp
      ),
    unemployment:
      firstNumber(
        fred?.macro?.unemployment,
        fallback.macro.unemployment
      ),
    population:
      firstNumber(
        worldBank?.macro?.population,
        fallback.macro.population
      ),
    tradePercentGdp:
      firstNumber(
        worldBank?.macro?.tradePercentGdp,
        fallback.macro.tradePercentGdp
      )
  };

  const signals = Array.isArray(live?.signals) && live.signals.length
    ? live.signals
    : fallback.signals;

  return {
    markets,
    macro,
    signals,
    source: buildSourceLabel({ live, fred, worldBank, commodity }),
    updatedAt: newestDate([
      live?.updatedAt,
      fred?.updatedAt,
      worldBank?.updatedAt,
      commodity?.updatedAt
    ]) || new Date().toISOString()
  };
}

function buildSourceLabel({ live, fred, worldBank, commodity }) {
  const labels = [];

  if (live) labels.push("live");
  if (fred) labels.push("fred");
  if (worldBank) labels.push("worldbank");
  if (commodity) labels.push("commodities");

  return labels.length ? labels.join("+") : "data-core-fallback";
}

function newestDate(values) {
  const valid = values
    .filter(Boolean)
    .map((value) => new Date(value))
    .filter((date) => !Number.isNaN(date.getTime()))
    .sort((a, b) => b.getTime() - a.getTime());

  return valid.length ? valid[0].toISOString() : null;
}

function pickValue(results, index) {
  const item = results[index];
  return item?.status === "fulfilled" ? item.value : null;
}

function firstNumber(...values) {
  for (const value of values) {
    const parsed = Number(value);
    if (Number.isFinite(parsed)) {
      return parsed;
    }
  }
  return null;
}

function toNumberOrNull(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function getFallbackData() {
  return {
    markets: {
      oil: 82.4,
      gold: 2188.2,
      sp500: 5128.4,
      interestRate: 4.75,
      shipping: 1460,
      copper: 4.1,
      wheat: 5.7
    },
    macro: {
      inflation: 3.2,
      gdp: 1000000000000,
      unemployment: 4.1,
      population: 85000000,
      tradePercentGdp: 56.0
    },
    signals: [
      {
        title: "Energy Pressure",
        severity: "high",
        category: "energy",
        summary: "Energy markets remain under pressure."
      },
      {
        title: "Logistics Stress",
        severity: "medium",
        category: "logistics",
        summary: "Shipping and route costs remain elevated."
      }
    ]
  };
}
