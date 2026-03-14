export function computeSignals(data) {
  let score = 0;

  if (data.markets.oil > 80) score += 30;
  if (data.markets.interestRate > 4.5) score += 20;

  data.signals.forEach(signal => {
    if (signal.severity === "high") score += 15;
    if (signal.severity === "medium") score += 8;
  });

  return {
    globalRiskScore: score,
    dominantDriver: data.dominantDriver,
    signals: data.signals,
    markets: data.markets
  };
    }
