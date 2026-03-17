export function buildOffer(trade) {
  return {
    id: "OFF-" + Date.now(),
    price: trade.amount,
    currency: "USD",
    status: "created"
  };
}
