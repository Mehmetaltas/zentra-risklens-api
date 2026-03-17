import { loadExtendedData } from "./dataEngine.js"
import { computeSignals } from "./signalEngine.js"

export async function runBrain() {
  try {
    const data = await loadExtendedData()

    if (!data) {
      console.error("NO DATA FROM ENGINE")
      return buildFallback()
    }

    const signalResult = computeSignals(data)

    return {
      riskScore: signalResult.globalRiskScore,
      riskLevel: signalResult.riskLevel,
      driver: signalResult.dominantDriver,

      markets: signalResult.markets,
      signals: signalResult.signals,

      advisory: buildAdvisory(signalResult.riskLevel),

      source: data.source || "unknown"
    }

  } catch (error) {
    console.error("BRAIN ERROR:", error)
    return buildFallback()
  }
}

function buildAdvisory(level) {
  if (level === "high") {
    return {
      shortTerm: "Tighten monitoring",
      midTerm: "Prepare hedge scenarios"
    }
  }

  if (level === "medium") {
    return {
      shortTerm: "Monitor key signals",
      midTerm: "Adjust exposure gradually"
    }
  }

  return {
    shortTerm: "System stable",
    midTerm: "Maintain positioning"
  }
}

function buildFallback() {
  return {
    riskScore: "--",
    riskLevel: "--",
    driver: "--",
    markets: {},
    signals: [],
    advisory: {
      shortTerm: "No data",
      midTerm: "No data"
    },
    source: "engine-error"
  }
}
