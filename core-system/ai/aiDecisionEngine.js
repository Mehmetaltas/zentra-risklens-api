
export function runAIDecisionEngine({ data, trade, cost, offer, logistics, security }) {
  const reasons = [];
  let score = 50;

  if ((data?.demand || "").toUpperCase() === "HIGH") {
    score += 15;
    reasons.push("High demand detected");
  }

  if ((trade?.profit || 0) > 15000) {
    score += 20;
    reasons.push("Trade profit above target threshold");
  }

  if ((cost?.totalCost || 0) < 1000) {
    score += 10;
    reasons.push("Operational cost remains controlled");
  }

  if ((logistics?.estimatedDays || 999) <= 25) {
    score += 10;
    reasons.push("Logistics time acceptable");
  }

  if ((security?.fraudRisk || "").toUpperCase() === "LOW") {
    score += 10;
    reasons.push("Fraud risk is low");
  }

  if (score > 100) score = 100;

  let recommendation = "HOLD";
  if (score >= 75) recommendation = "EXECUTE";
  else if (score >= 60) recommendation = "REVIEW";

  return {
    aiDecisionScore: score,
    recommendation,
    reasons,
    confidence: score >= 75 ? "HIGH" : score >= 60 ? "MEDIUM" : "LOW"
  };
}
