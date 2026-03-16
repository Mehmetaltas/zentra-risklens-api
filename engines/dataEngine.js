export function loadExtendedData() {
  return {
    system: {
      name: "ZENTRA",
      mode: "V1",
      status: "operational"
    },

    markets: {
      oil: 82.4,
      gold: 2180.5,
      sp500: 5120.3,
      interestRate: 4.75,
      shipping: 1460
    },

    signals: [
      { title: "Energy Pressure", severity: "high", category: "energy" },
      { title: "Logistics Stress", severity: "medium", category: "logistics" },
      { title: "Market Stress", severity: "low", category: "markets" }
    ],

    finance: {
      liquidityPressure: "medium",
      ratePressure: "high",
      volatility: "medium"
    },

    trade: {
      routeStress: "medium",
      customsPressure: "low",
      supplyPressure: "medium"
    },

    dominantDriver: "Energy Pressure"
  };
}
