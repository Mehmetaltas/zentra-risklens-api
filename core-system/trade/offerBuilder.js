export function buildOffer(trade, cost) {
  return {
    product: trade.product,
    finalPrice: trade.sellPrice,
    cost: cost.totalCost,
    netProfit: trade.totalProfit - cost.totalCost,
    status: "OFFER_READY"
  };
}
