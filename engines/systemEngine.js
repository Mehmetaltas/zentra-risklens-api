import { loadExtendedData } from "./dataEngine.js";
import { computeSignals } from "./signalEngine.js";
import { computeRisk } from "./riskEngine.js";
import { strategicAdvisory } from "./decisionEngine.js";
import { marketSummary } from "./marketEngine.js";

import { computeFinance } from "./financeEngine.js";
import { computeTradeIntelligence } from "./tradeIntelligenceEngine.js";
import { computeOpportunities } from "./opportunityEngine.js";
import { executionPlan } from "./executionEngine.js";
import { buildKnowledgeGraph } from "./knowledgeGraphEngine.js";
import { evolutionState } from "./evolutionEngine.js";

export async function runZentra() {
  const data = await loadExtendedData();

  const signalScore = computeSignals(data);
  const risk = computeRisk(signalScore);
  const advisory = strategicAdvisory(risk);
  const market = marketSummary(data.markets);

  const finance = computeFinance(data);
  const trade = computeTradeIntelligence(data);
  const opportunities = computeOpportunities(data, risk, finance, trade);
  const execution = executionPlan(risk, finance, trade);
  const knowledgeGraph = buildKnowledgeGraph(data);
  const evolution = evolutionState();

  return {
    data,
    signalScore,
    risk,
    advisory,
    market,
    finance,
    trade,
    opportunities,
    execution,
    knowledgeGraph,
    evolution
  };
}
