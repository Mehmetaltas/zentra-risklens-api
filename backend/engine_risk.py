from typing import Dict, Any, List


def calculate_risk_score(signals_payload: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    signals = signals_payload["signals"]
    if not signals:
        return {
            "risk_score": 0,
            "stress_probability": 0.0,
            "confidence": 0.0,
            "category": "normal"
        }

    avg_score = sum(item["score"] for item in signals) / len(signals)

    if avg_score >= 70:
        category = "high"
    elif avg_score >= 55:
        category = "elevated"
    else:
        category = "normal"

    return {
        "risk_score": round(avg_score),
        "stress_probability": round(avg_score / 100, 2),
        "confidence": 0.81,
        "category": category
    }


def explain_risk(signals_payload: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    signals = signals_payload["signals"]
    drivers = [item["id"].replace("_", " ") for item in signals if item["score"] >= 50]

    return {
        "drivers": drivers,
        "summary": "Risk is elevated due to cost pressure and logistics strain."
        if drivers else "Risk remains within normal conditions."
    }
