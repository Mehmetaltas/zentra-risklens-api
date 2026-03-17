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
  try {
    const data = await loadExtendedData();

    if (!data) {
      throw new Error("Data engine returned empty data");
    }

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
  } catch (error) {
    console.error("SYSTEM ENGINE ERROR:", error);

    const fallbackData = {
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
      source: "system-fallback",
      updatedAt: null
    };

    const signalScore = computeSignals(fallbackData);
    const risk = computeRisk(signalScore);
    const advisory = strategicAdvisory(risk);
    const market = marketSummary(fallbackData.markets);

    const finance = computeFinance(fallbackData);
    const trade = computeTradeIntelligence(fallbackData);
    const opportunities = computeOpportunities(
      fallbackData,
      risk,
      finance,
      trade
    );
    const execution = executionPlan(risk, finance, trade);
    const knowledgeGraph = buildKnowledgeGraph(fallbackData);
    const evolution = evolutionState();

    return {
      data: fallbackData,
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
}
