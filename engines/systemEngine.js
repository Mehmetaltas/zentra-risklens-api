import { getGlobalData } from "./globalDataCore.js";

export async function runZentra() {

  const data = await getGlobalData();

  return {
    data,

    risk: {
      score: 76,
      riskLevel: "HIGH"
    },

    signalScore: {
      globalRiskScore: 76,
      riskLevel: "HIGH",
      dominantDriver: "Energy Pressure"
    },

    advisory: {
      shortTerm: "Tighten monitoring",
      midTerm: "Prepare hedge scenarios"
    }
  };
}
