export function createTrade(data) {
  const margin = data.sellPrice - data.buyPrice;

  return {
    product: data.product,
    volume: data.volume,
    buyPrice: data.buyPrice,
    sellPrice: data.sellPrice,
    margin,
    totalProfit: margin * data.volume,
    status: "CREATED"
  };
}
