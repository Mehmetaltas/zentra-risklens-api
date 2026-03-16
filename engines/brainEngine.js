import { runZentra } from "./systemEngine.js"

export function runBrain(){

const result = runZentra()

return {
riskScore: result.risk.score,
riskLevel: result.risk.riskLevel,
driver: result.data.dominantDriver,
markets: result.data.markets,
signals: result.data.signals,
advisory: result.advisory
}

}
