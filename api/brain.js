export default function handler(req,res){

const inflation=5+Math.random()*2
const rate=4+Math.random()*1
const volatility=40+Math.random()*10
const liquidity=60+Math.random()*10

const risk=
inflation*0.3+
rate*0.2+
volatility*0.3+
(100-liquidity)*0.2

res.status(200).json({
risk:Math.round(risk),
state:"Moderate Pressure",
trend:"Neutral",
advice:"Control costs and diversify risks."
})

}
