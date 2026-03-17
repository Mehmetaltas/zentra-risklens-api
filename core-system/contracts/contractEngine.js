export function generateContract(trade) {
  return {
    contractId: "CONTRACT-" + Date.now(),
    product: trade.product,
    volume: trade.volume,
    status: "GENERATED"
  };
}
