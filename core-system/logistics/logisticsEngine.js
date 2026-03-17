export function planLogistics(trade) {
  return {
    mode: "SEA",
    estimatedDays: 25,
    cost: trade.volume * 3
  };
}
