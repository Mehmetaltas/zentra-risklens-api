export function computeFinance(data) {
  let financeScore = 0;

  if ((data.markets.interestRate || 0) > 4.5) financeScore += 35;
  if (data.finance.liquidityPressure === "medium") financeScore += 20;
  if (data.finance.ratePressure === "high") financeScore += 30;
  if (data.finance.volatility === "medium") financeScore += 15;

  if (financeScore > 100) financeScore = 100;

  let financeLevel = "low";
  if (financeScore >= 70) financeLevel = "high";
  else if (financeScore >= 40) financeLevel = "medium";

  return {
    financeScore,
    financeLevel,
    summary: "Finance pressure calculated"
  };
}
