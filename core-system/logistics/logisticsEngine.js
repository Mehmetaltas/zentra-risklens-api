export function planLogistics(trade) {
  return {
    mode: "MULTI", // sea + air + land
    route: "AUTO_OPTIMIZED",
    duration: "10-20 days",
    costEstimate: trade.volume * 12,
    status: "PLANNED"
  };
}
