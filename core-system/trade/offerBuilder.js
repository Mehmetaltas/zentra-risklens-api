export function buildOffer(trade, cost) {
  return {
    product: trade.product,
    volume: trade.volume,
    totalCost: cost.totalCost,
    sellValue: trade.sellPrice * trade.volume,
    netProfit: (trade.sellPrice * trade.volume) - cost.totalCost
  };
}
