export function calculateCost(trade) {
  const logisticsCost = trade.volume * 10;
  const tax = trade.totalProfit * 0.1;

  return {
    logisticsCost,
    tax,
    totalCost: logisticsCost + tax
  };
}
