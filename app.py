from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import uuid
import datetime

app = FastAPI(
    title="Zentra RiskLens API",
    version="1.1",
    description="AI-powered modular risk scoring infrastructure"
)

# =========================
# API KEY SYSTEM
# =========================

VALID_API_KEYS = {
    "zentra-demo-key",
    "zentra-partner-key"
}

# =========================
# REQUEST MODEL
# =========================

class RiskRequest(BaseModel):
    amount: float
    sector: str
    sector_risk_level: int      # 1–5
    payment_delay_days: int
    customer_score: int         # 0–100
    exposure_ratio: float       # 0–1

# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "zentra-risklens",
        "timestamp": datetime.datetime.utcnow()
    }

# =========================
# RISK ENGINE v1.1
# =========================

@app.post("/v1/risk")
def calculate_risk(
    request: RiskRequest,
    x_api_key: str = Header(None)
):

    # API KEY VALIDATION
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # -------------------------
    # RISK WEIGHTS CALCULATION
    # -------------------------

    amount_weight = min((request.amount / 50000) * 25, 25)
    sector_weight = (request.sector_risk_level / 5) * 20
    delay_weight = min((request.payment_delay_days / 60) * 25, 25)
    behavior_weight = ((100 - request.customer_score) / 100) * 20
    exposure_weight = request.exposure_ratio * 10

    risk_score = (
        amount_weight +
        sector_weight +
        delay_weight +
        behavior_weight +
        exposure_weight
    )

    # -------------------------
    # RISK LEVEL CLASSIFICATION
    # -------------------------

    if risk_score < 30:
        level = "Low"
    elif risk_score < 60:
        level = "Medium"
    else:
        level = "High"

    # -------------------------
    # RESPONSE
    # -------------------------

    return {
        "request_id": str(uuid.uuid4()),
        "model_version": "1.1",
        "risk_score": round(risk_score, 2),
        "risk_level": level,
        "risk_factors": {
            "amount_weight": round(amount_weight, 2),
            "sector_weight": round(sector_weight, 2),
            "delay_weight": round(delay_weight, 2),
            "behavior_weight": round(behavior_weight, 2),
            "exposure_weight": round(exposure_weight, 2)
        },
        "confidence": 0.91,
        "timestamp": datetime.datetime.utcnow()
    }
