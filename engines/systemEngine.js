import { getGlobalData } from "./globalDataCore.js";

export async function runZentra() {
  const data = await getGlobalData();

  const risk = buildRisk(data);
  const signalScore = buildSignalScore(data, risk);
  const advisory = buildAdvisory(risk);
  const market = buildMarketSummary(data);

  return {
    data,
    risk,
    signalScore,
    advisory,
    market,
    finance: {},
    trade: {},
    opportunities: [],
    execution: {},
    knowledgeGraph: {},
    evolution: {}
  };
}

function buildRisk(data) {
  let score = 0;

  if ((data?.markets?.oil || 0) > 80) score += 20;
  if ((data?.markets?.shipping || 0) > 1400) score += 20;
  if ((data?.markets?.interestRate || 0) > 4.5) score += 15;
  if ((data?.macro?.inflation || 0) > 3) score += 15;
  if ((data?.signals || []).length >= 2) score += 15;
  if ((data?.markets?.sp500 || 0) < 5200) score += 10;
  if ((data?.macro?.tradePercentGdp || 0) > 50) score += 5;

  if (score > 100) score = 100;

  let riskLevel = "LOW";
  if (score >= 70) riskLevel = "HIGH";
  else if (score >= 40) riskLevel = "MEDIUM";

  return {
    score,
    riskLevel
  };
}

function buildSignalScore(data, risk) {
  return {
    globalRiskScore: risk.score,
    riskLevel: risk.riskLevel,
    dominantDriver:
      data?.signals?.[0]?.title ||
      inferDriver(data)
  };
}

function inferDriver(data) {
  if ((data?.markets?.oil || 0) > 80) return "Energy Pressure";
  if ((data?.markets?.shipping || 0) > 1400) return "Logistics Stress";
  return "Stable Conditions";
}

function buildAdvisory(risk) {
  if (risk.riskLevel === "HIGH") {
    return {
      shortTerm: "Tighten monitoring",
      midTerm: "Prepare hedge scenarios"
    };
  }

  if (risk.riskLevel === "MEDIUM") {
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

function buildMarketSummary(data) {
  return {
    oil: data?.markets?.oil ?? null,
    gold: data?.markets?.gold ?? null,
    sp500: data?.markets?.sp500 ?? null,
    interestRate: data?.markets?.interestRate ?? null,
    shipping: data?.markets?.shipping ?? null,
    inflation: data?.macro?.inflation ?? null,
    gdp: data?.macro?.gdp ?? null
  };
      }
