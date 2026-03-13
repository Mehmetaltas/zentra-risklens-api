// ZENTRA Source Registry
// Global veri kaynaklarının listesi

export const SOURCES = {

  energy: [
    {
      id: "oil_price",
      name: "Global Oil Price",
      unit: "USD",
      fallback: 82
    }
  ],

  logistics: [
    {
      id: "container_rate",
      name: "Container Shipping Rate",
      unit: "USD",
      fallback: 2100
    }
  ],

  finance: [
    {
      id: "inflation",
      name: "Global Inflation Estimate",
      unit: "%",
      fallback: 5.4
    }
  ],

  cyber: [
    {
      id: "cyber_risk",
      name: "Cyber Threat Level",
      unit: "index",
      fallback: 58
    }
  ]

}


// Basit veri yükleme fonksiyonu
export function loadSources() {

  const data = {}

  Object.keys(SOURCES).forEach(group => {

    data[group] = SOURCES[group].map(src => {
      return {
        id: src.id,
        name: src.name,
        value: src.fallback,
        unit: src.unit
      }
    })

  })

  return data
}
