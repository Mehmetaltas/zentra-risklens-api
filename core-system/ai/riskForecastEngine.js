export function runRiskForecastEngine({ data, logistics, security }) {
  const oil = data?.markets?.oil ?? 82.4;
  const shipping = data?.markets?.shipping ?? 1460;
  const fraudRisk = (security?.fraudRisk || "LOW").toUpperCase();
  const days = logistics?.estimatedDays || 25;

  let forecastScore = 40;
  const forecastDrivers = [];

  if (oil > 80) {
    forecastScore += 15;
    forecastDrivers.push("Energy pressure remains elevated");
  }

  if (shipping > 1400) {
    forecastScore += 20;
    forecastDrivers.push("Shipping costs remain high");
  }

  if (days > 20) {
    forecastScore += 10;
    forecastDrivers.push("Transit duration may increase exposure");
  }

  if (fraudRisk === "LOW") {
    forecastScore -= 5;
    forecastDrivers.push("Fraud risk remains under control");
  }

  if (forecastScore < 0) forecastScore = 0;
  if (forecastScore > 100) forecastScore = 100;

  let forecastLevel = "LOW";
  if (forecastScore >= 70) forecastLevel = "HIGH";
  else if (forecastScore >= 45) forecastLevel = "MEDIUM";

  return {
    riskForecastScore: forecastScore,
    riskForecastLevel: forecastLevel,
    forecastDrivers,
    horizon: "30D"
  };
}
