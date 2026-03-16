export function computeRisk(score){

let riskLevel="low"

if(score>=70) riskLevel="high"
else if(score>=40) riskLevel="medium"

let summary="System stable"

if(riskLevel==="high")
summary="Global stress elevated"

if(riskLevel==="medium")
summary="Moderate systemic pressure"

return {
score,
riskLevel,
summary
}

}
