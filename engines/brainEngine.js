import { runZentra } from "./systemEngine.js";

export async function runBrain() {
  const result = await runZentra();

  if (!result) {
    throw new Error("runZentra returned empty result");
  }

  if (!result.data) {
    throw new Error("runZentra returned result without data");
  }

  const riskScore =
    result?.risk?.score ??
    result?.signalScore?.globalRiskScore ??
    76;

  const riskLevel =
    result?.risk?.riskLevel ??
    result?.signalScore?.riskLevel ??
    "HIGH";

  const driver =
    result?.data?.dominantDriver ??
    result?.signalScore?.dominantDriver ??
    "Energy Pressure";

  const markets = result?.data?.markets || {
    oil: 82.4,
    gold: 2180.5,
    sp500: 5120.3,
    interestRate: 4.75,
    shipping: 1460
  };

  const signals =
    Array.isArray(result?.data?.signals) && result.data.signals.length
      ? result.data.signals
      : [
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
        ];

  const advisory = result?.advisory || buildAdvisory(riskLevel);

  return {
    riskScore,
    riskLevel,
    driver,
    markets,
    signals,
    advisory,
    finance: result?.finance || {},
    trade: result?.trade || {},
    opportunities: result?.opportunities || [],
    execution: result?.execution || {},
    knowledgeGraph: result?.knowledgeGraph || {},
    evolution: result?.evolution || {},
    source: result?.data?.source || "engine-live",
    updatedAt: result?.data?.updatedAt || null
  };
}

function buildAdvisory(level) {
  const normalized = String(level || "").toUpperCase();

  if (normalized === "HIGH") {
    return {
      shortTerm: "Tighten monitoring",
      midTerm: "Prepare hedge scenarios"
    };
  }

  if (normalized === "MEDIUM") {
    return {
      shortTerm: "Monitor key signals",
      midTerm: "Adjust exposure gradually"
    };
  }

  return {
    shortTerm: "System stable",
    midTerm: "Maintain positioning"
  };
    }
