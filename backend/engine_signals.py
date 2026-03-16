from typing import Dict, Any, List


def build_signals(market: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    oil = market["oil"]
    shipping = market["shipping"]
    interest = market["interest"]

    energy_pressure_score = 64 if oil > 80 else 38
    logistics_stress_score = 72 if shipping > 1400 else 43
    market_stress_score = 41 if interest < 5 else 58

    signals = [
        {
            "id": "energy_pressure",
            "title": "Energy Pressure",
            "severity": _severity_from_score(energy_pressure_score),
            "score": energy_pressure_score,
            "summary": "Energy costs are rising."
        },
        {
            "id": "logistics_stress",
            "title": "Logistics Stress",
            "severity": _severity_from_score(logistics_stress_score),
            "score": logistics_stress_score,
            "summary": "Shipping conditions are tightening."
        },
        {
            "id": "market_stress",
            "title": "Market Stress",
            "severity": _severity_from_score(market_stress_score),
            "score": market_stress_score,
            "summary": "Market volatility remains moderate."
        }
    ]

    return {"signals": signals}


def _severity_from_score(score: int) -> str:
    if score >= 70:
        return "high"
    if score >= 50:
        return "medium"
    return "low"
