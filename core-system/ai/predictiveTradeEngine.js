export function runPredictiveTradeEngine({ data, trade, offer }) {
  const baseDemand = (data?.demand || "").toUpperCase();
  const currentProfit = trade?.profit || 0;
  const sellValue = offer?.sellValue || 0;

  let nextTrend = "STABLE";
  let projectedProfit = currentProfit;
  let projectedSellValue = sellValue;

  if (baseDemand === "HIGH") {
    nextTrend = "UP";
    projectedProfit = Math.round(currentProfit * 1.12);
    projectedSellValue = Math.round(sellValue * 1.08);
  } else if (baseDemand === "LOW") {
    nextTrend = "DOWN";
    projectedProfit = Math.round(currentProfit * 0.9);
    projectedSellValue = Math.round(sellValue * 0.94);
  }

  return {
    nextTrend,
    projectedProfit,
    projectedSellValue,
    timeHorizon: "30D",
    predictiveSignal: nextTrend === "UP" ? "EXPAND" : nextTrend === "DOWN" ? "REDUCE" : "MONITOR"
  };
}
