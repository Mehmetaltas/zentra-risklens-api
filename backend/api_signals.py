from fastapi import APIRouter
from backend.data_provider import get_market_summary
from backend.engine_signals import build_signals

router = APIRouter(prefix="/api", tags=["signals"])


@router.get("/signals")
def get_signals():
    market = get_market_summary()
    return build_signals(market)
