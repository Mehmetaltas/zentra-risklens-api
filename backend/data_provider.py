from typing import Dict, Any


def get_market_summary() -> Dict[str, Any]:
    return {
        "oil": 82.4,
        "gold": 2180.5,
        "sp500": 5120.3,
        "interest": 4.75,
        "shipping": 1460,
        "status": "ok"
    }


def get_market_indicators() -> Dict[str, Any]:
    data = get_market_summary()
    return {
        "items": [
            {"key": "oil", "label": "Oil", "value": data["oil"]},
            {"key": "gold", "label": "Gold", "value": data["gold"]},
            {"key": "sp500", "label": "S&P 500", "value": data["sp500"]},
            {"key": "interest", "label": "Interest", "value": data["interest"]},
            {"key": "shipping", "label": "Shipping", "value": data["shipping"]},
        ]
    }
