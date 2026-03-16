export function computeSignals(data) {
  let score = 0;

  const markets = data?.markets || {};
  const signals = data?.signals || [];
  const dominantDriver = data?.dominantDriver || "unknown";

  if ((markets.oil || 0) > 80) score += 30;
  if ((markets.interestRate || 0) > 4.5) score += 20;

  signals.forEach(signal => {
    if (signal.severity === "high") score += 15;
    if (signal.severity === "medium") score += 8;
    if (signal.severity === "low") score += 3;
  });

  if (score > 100) score = 100;

  let riskLevel = "low";
  if (score >= 70) riskLevel = "high";
  else if (score >= 40) riskLevel = "medium";

  let summary = "System conditions are stable.";
  if (riskLevel === "high") {
    summary = "Global stress is elevated due to market and signal pressure.";
  } else if (riskLevel === "medium") {
    summary = "System shows moderate stress across key indicators.";
  }

  return {
    globalRiskScore: score,
    riskLevel,
    dominantDriver,
    summary,
    signals,
    markets
  };
}
