export function computeOpportunities(data, risk, finance, trade) {
  const opportunities = [];

  if (risk.riskLevel === "high") {
    opportunities.push("Defensive monitoring products");
  }

  if (finance.financeLevel === "high") {
    opportunities.push("Treasury and hedging intelligence");
  }

  if (trade.tradeLevel === "medium" || trade.tradeLevel === "high") {
    opportunities.push("Route optimization and trade visibility");
  }

  if (opportunities.length === 0) {
    opportunities.push("Baseline market observation");
  }

  return {
    opportunities,
    count: opportunities.length
  };
}
