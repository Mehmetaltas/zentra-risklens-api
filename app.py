# ==============================
# Zentra RiskLens API v1.2
# Production Guardrails Edition
# ==============================

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
import uuid
import datetime
import logging

app = FastAPI(
    title="Zentra RiskLens API",
    version="1.2",
    description="AI-powered modular risk scoring infrastructure"
)

# =========================
# LOGGING CONFIG
# =========================
logging.basicConfig(level=logging.INFO)

# =========================
# API KEY SYSTEM
# =========================
VALID_API_KEYS = {
    "zentra-demo-key",
    "zentra-partner-key"
}

# =========================
# REQUEST MODEL (Guarded)
# =========================
class RiskRequest(BaseModel):
    amount: float = Field(gt=0, le=10_000_000)
    sector: str
    sector_risk_level: int = Field(ge=1, le=5)
    payment_delay_days: int = Field(ge=0, le=365)
    customer_score: int = Field(ge=0, le=100)
    exposure_ratio: float = Field(ge=0, le=1)

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {
        "status": "Zentra RiskLens API is live",
        "version": "1.2"
    }

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
# RISK ENGINE v1.2
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
    # RISK WEIGHTS
    # -------------------------
    amount_weight = min((request.amount / 50000) * 25, 25)
    sector_weight = (request.sector_risk_level / 5) * 20
    delay_weight = min((request.payment_delay_days / 60) * 25, 25)
    behavior_weight = ((100 - request.customer_score) / 100) * 15
    exposure_weight = request.exposure_ratio * 15

    risk_score = (
        amount_weight +
        sector_weight +
        delay_weight +
        behavior_weight +
        exposure_weight
    )

    # -------------------------
    # RISK LEVEL
    # -------------------------
    if risk_score < 30:
        level = "Low"
    elif risk_score < 60:
        level = "Medium"
    else:
        level = "High"

    logging.info(f"Risk calculated: {risk_score} | Level: {level}")

    # -------------------------
    # RESPONSE
    # -------------------------
    return {
        "request_id": str(uuid.uuid4()),
        "model_version": "1.2",
        "risk_score": round(risk_score, 2),
        "risk_level": level,
        "risk_factors": {
            "amount_weight": round(amount_weight, 2),
            "sector_weight": round(sector_weight, 2),
            "delay_weight": round(delay_weight, 2),
            "behavior_weight": round(behavior_weight, 2),
            "exposure_weight": round(exposure_weight, 2)
        },
        "confidence": 0.93,
        "timestamp": datetime.datetime.utcnow()
    }
