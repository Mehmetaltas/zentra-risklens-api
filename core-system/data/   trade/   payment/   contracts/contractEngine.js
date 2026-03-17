export function createContract(trade) {
  return {
    id: "CNT-" + Date.now(),
    buyer: trade.buyer,
    seller: trade.seller,
    amount: trade.amount,
    status: "draft"
  };
}
