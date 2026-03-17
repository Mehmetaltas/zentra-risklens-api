export function generateContract(trade) {
  return {
    contractId: "CTR_" + Date.now(),
    product: trade.product,
    parties: ["Buyer", "Seller"],
    value: trade.sellPrice * trade.volume,
    status: "SIGNED"
  };
}
