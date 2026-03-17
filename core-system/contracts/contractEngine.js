export function generateContract(trade) {
  return {
    product: trade.product,
    volume: trade.volume,
    status: "GENERATED"
  };
}
