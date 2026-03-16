
from fastapi import APIRouter
from backend.data_provider import get_market_summary
from backend.engine_signals import build_signals
from backend.engine_risk import calculate_risk_score

router = APIRouter(prefix="/api/terminal", tags=["terminal"])


@router.get("/overview")
def terminal_overview():
    market = get_market_summary()
    signals_payload = build_signals(market)
    risk_payload = calculate_risk_score(signals_payload)

    signal_map = {item["id"]: item["score"] for item in signals_payload["signals"]}

    return {
        "market": {
            "oil": market["oil"],
            "gold": market["gold"],
            "sp500": market["sp500"],
            "interest": market["interest"],
            "shipping": market["shipping"]
        },
        "signals": signal_map,
        "risk": risk_payload,
        "system_status": "ok"
    }
