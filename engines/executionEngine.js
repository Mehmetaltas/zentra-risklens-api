
export function executionPlan(risk, finance, trade) {
  const actions = [];

  if (risk.riskLevel === "high") {
    actions.push("Tighten risk monitoring");
  }

  if (finance.financeLevel === "high") {
    actions.push("Review financing and liquidity scenarios");
  }

  if (trade.tradeLevel === "high") {
    actions.push("Review logistics routes and shipment exposure");
  }

  if (actions.length === 0) {
    actions.push("Maintain standard monitoring");
  }

  return {
    actions,
    actionCount: actions.length
  };
}
