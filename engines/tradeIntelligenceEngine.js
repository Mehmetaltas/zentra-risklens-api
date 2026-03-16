export function computeTradeIntelligence(data) {
  let tradeScore = 0;

  if (data.trade.routeStress === "medium") tradeScore += 25;
  if (data.trade.customsPressure === "low") tradeScore += 10;
  if (data.trade.supplyPressure === "medium") tradeScore += 25;
  if ((data.markets.shipping || 0) > 1200) tradeScore += 30;

  if (tradeScore > 100) tradeScore = 100;

  let tradeLevel = "low";
  if (tradeScore >= 70) tradeLevel = "high";
  else if (tradeScore >= 40) tradeLevel = "medium";

  return {
    tradeScore,
    tradeLevel,
    summary: "Trade pressure calculated"
  };
}
