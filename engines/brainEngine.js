import { runZentra } from "./systemEngine.js";

export async function runBrain() {
  const result = await runZentra();

  return {
    riskScore: result.risk.score,
    riskLevel: result.risk.riskLevel,
    driver: result.data.dominantDriver,

    markets: result.data.markets,
    signals: result.data.signals,
    advisory: result.advisory,

    finance: result.finance,
    trade: result.trade,
    opportunities: result.opportunities,
    execution: result.execution,
    knowledgeGraph: result.knowledgeGraph,
    evolution: result.evolution,

    source: result.data.source || "unknown"
  };
}
