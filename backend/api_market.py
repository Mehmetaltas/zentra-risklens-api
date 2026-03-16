from fastapi import APIRouter
from backend.data_provider import get_market_summary, get_market_indicators

router = APIRouter(prefix="/api/market", tags=["market"])


@router.get("/summary")
def market_summary():
    return get_market_summary()


@router.get("/indicators")
def market_indicators():
    return get_market_indicators()
