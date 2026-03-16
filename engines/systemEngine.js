import {loadGlobalData} from "./dataEngine.js"
import {computeSignals} from "./signalEngine.js"
import {computeRisk} from "./riskEngine.js"
import {strategicAdvisory} from "./decisionEngine.js"

export function runZentra(){

const data = loadGlobalData()

const signalScore = computeSignals(data)

const risk = computeRisk(signalScore)

const advisory = strategicAdvisory(risk)

return {
data,
risk,
advisory
}

}
