export function createInsurance(trade) {
  return {
    type: "FULL",
    cost: trade.amount * 0.02,
    status: "active"
  };
}
