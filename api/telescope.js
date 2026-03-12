export default async function handler(req, res) {
  const data = {
    timestamp: new Date().toISOString(),

    global_risk_score: 72,
    dominant_driver: "oil_shock",
    system_state: "elevated",

    energy: {
      oil_price: 82,
      gas_price: 3.1,
      pressure: "elevated"
    },

    logistics: {
      container_rate: 4200,
      port_delay: 1.4,
      stress: "high"
    },

    cyber: {
      threat_level: "elevated",
      active_incidents: 12
    },

    satellite: {
      shipping_activity: "normal",
      port_activity_index: 74
    },

    signals: [
      {
        key: "oil_shock",
        severity: "high",
        confidence: "medium",
        message: "Oil price pressure increasing",
        affects: ["aviation", "logistics", "inflation"]
      },
      {
        key: "shipping_congestion",
        severity: "high",
        confidence: "medium",
        message: "Container shipping costs rising",
        affects: ["trade", "supply_chain", "retail"]
      },
      {
        key: "cyber_risk",
        severity: "medium",
        confidence: "medium",
        message: "Cyber threat activity elevated",
        affects: ["payments", "banking", "infrastructure"]
      },
      {
        key: "port_stress",
        severity: "medium",
        confidence: "low",
        message: "Port activity pressure detected",
        affects: ["shipping", "routes", "throughput"]
      }
    ]
  };

  res.status(200).json(data);
}

