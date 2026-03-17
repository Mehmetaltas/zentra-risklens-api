export function initiatePayment(trade) {
  return {
    amount: trade.sellPrice * trade.volume,
    currency: "USD",
    method: "SWIFT",
    status: "INITIATED"
  };
}
