export function calculateCost(trade) {
  const logistics = trade.volume * 5;
  const tax = trade.buyPrice * 0.1;

  return {
    logistics,
    tax,
    totalCost: logistics + tax
  };
}
