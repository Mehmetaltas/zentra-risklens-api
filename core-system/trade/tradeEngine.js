export function createTrade({ product, buyPrice, sellPrice, volume }) {
  return {
    product,
    buyPrice,
    sellPrice,
    volume,
    profit: (sellPrice - buyPrice) * volume
  };
}
