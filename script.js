function updateRisk(){

let risk=Math.floor(Math.random()*100)

document.getElementById("riskScore").innerText=risk

if(risk>70){

state.innerText="High Risk"
trend.innerText="Bearish"

}else if(risk>40){

state.innerText="Moderate"
trend.innerText="Neutral"

}else{

state.innerText="Stable"
trend.innerText="Bullish"

}

}

setInterval(updateRisk,4000)


function runScenario(){

let s=document.getElementById("scenarioName").value

scenarioResult.innerText=
"Scenario: "+s+"\nProjected Risk Impact +15"

}


function runSME(){

let r=Number(smeRevenue.value)

let c=Number(smeCost.value)

let d=Number(smeDebt.value)

let profit=r-c-d

smeResult.innerText="Profit: "+profit

}


function runTrade(){

let o=tradeOrigin.value

let d=tradeDestination.value

let p=tradeProduct.value

tradeResult.innerText=
"Route: "+o+" → "+d+"\nProduct: "+p

}


function askChat(){

let q=chatInput.value

chatBox.innerHTML+=
"<br><b>You:</b>"+q+
"<br><b>ZENTRA:</b> analyzing..."

chatInput.value=""

  }
