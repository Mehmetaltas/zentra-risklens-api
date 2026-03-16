from fastapi import APIRouter
from backend.data_provider import get_market_summary
from backend.engine_signals import build_signals
from backend.engine_risk import calculate_risk_score, explain_risk

router = APIRouter(prefix="/api/risk", tags=["risk"])


@router.get("/score")
def risk_score():
    market = get_market_summary()
    signals_payload = build_signals(market)
    return calculate_risk_score(signals_payload)


@router.get("/explain")
def risk_explain():
    market = get_market_summary()
    signals_payload = build_signals(market)
    return explain_risk(signals_payload)


@router.get("/health")
def risk_health():
    return {
        "service": "risk",
        "status": "ok"
    }
