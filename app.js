export default function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET,OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  const inflation = 5 + Math.random() * 2;
  const rate = 4 + Math.random() * 1;
  const volatility = 40 + Math.random() * 10;
  const liquidity = 60 + Math.random() * 10;

  const risk =
    inflation * 0.3 +
    rate * 0.2 +
    volatility * 0.3 +
    (100 - liquidity) * 0.2;

  const sectors = [
    { sector: "Energy", risk: Math.floor(Math.random() * 100) },
    { sector: "Finance", risk: Math.floor(Math.random() * 100) },
    { sector: "Technology", risk: Math.floor(Math.random() * 100) },
    { sector: "Agriculture", risk: Math.floor(Math.random() * 100) },
    { sector: "Manufacturing", risk: Math.floor(Math.random() * 100) }
  ];

  const scenarios = [
    { scenario: "Interest Rate Shock", impact: "High" },
    { scenario: "Supply Chain Disruption", impact: "Medium" },
    { scenario: "Energy Crisis", impact: "High" },
    { scenario: "Currency Volatility", impact: "Medium" },
    { scenario: "Regional Conflict", impact: "Critical" }
  ];

  const opportunities = [
    { country: "Germany", sector: "Manufacturing" },
    { country: "UAE", sector: "Trade" },
    { country: "USA", sector: "Technology" },
    { country: "Turkey", sector: "Energy" },
    { country: "Singapore", sector: "Logistics" }
  ];

  const trade = [
    { from: "Turkey", to: "Germany", product: "Machinery" },
    { from: "China", to: "USA", product: "Electronics" },
    { from: "Brazil", to: "EU", product: "Agriculture" },
    { from: "India", to: "UAE", product: "Textile" }
  ];

  const careers = [
    { field: "AI Engineering", demand: "Very High" },
    { field: "Data Science", demand: "High" },
    { field: "Logistics", demand: "High" },
    { field: "Cyber Security", demand: "Very High" }
  ];

  return res.status(200).json({
    brain: {
      risk: Math.round(risk),
      state: "Moderate Pressure",
      trend: "Neutral",
      advice: "Control costs and diversify risks."
    },
    economic: {
      inflation: inflation.toFixed(2),
      rate: rate.toFixed(2),
      volatility: volatility.toFixed(0),
      liquidity: liquidity.toFixed(0)
    },
    sectors,
    scenarios,
    opportunities,
    trade,
    careers
  });
    }
