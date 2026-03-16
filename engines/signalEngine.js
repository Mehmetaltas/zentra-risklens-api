export function computeSignals(data){

let score = 0

if(data.markets.oil > 80) score += 30
if(data.markets.interestRate > 4.5) score += 20

data.signals.forEach(s => {

if(s.severity==="high") score += 15
if(s.severity==="medium") score += 8
if(s.severity==="low") score += 3

})

return score

}
