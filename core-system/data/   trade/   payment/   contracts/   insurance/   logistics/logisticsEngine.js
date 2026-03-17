export function planLogistics(trade) {
  return {
    mode: "sea",
    cost: trade.amount * 0.05,
    status: "planned"
  };
}
