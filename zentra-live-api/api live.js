export default async function handler(req, res) {

  try {

    const oilRes = await fetch("https://api.eia.gov/v2/petroleum/pri/spt/data/?frequency=daily&data[0]=value&sort[0][column]=period&sort[0][direction]=desc&length=1&api_key=DEMO_KEY")
    const oilData = await oilRes.json()

    const oil = oilData?.response?.data?.[0]?.value || 80

    const markets = {
      oil: oil,
      gold: 2180 + Math.random()*20,
      sp500: 5100 + Math.random()*80,
      interestRate: 4.5 + Math.random()*0.5,
      shipping: 1400 + Math.random()*300
    }

    const signals = []

    if (markets.oil > 80) {
      signals.push({
        title: "Energy Pressure",
        severity: "high",
        category: "energy",
        summary: "Energy markets under pressure."
      })
    }

    if (markets.shipping > 1500) {
      signals.push({
        title: "Logistics Stress",
        severity: "medium",
        category: "logistics",
        summary: "Shipping costs increasing."
      })
    }

    if (signals.length === 0) {
