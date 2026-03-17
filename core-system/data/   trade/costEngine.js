export function calculateCost(trade) {
  return {
    base: trade.amount,
    logistics: trade.amount * 0.05,
    insurance: trade.amount * 0.02
  };
}
