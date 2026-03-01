# Zentra RiskLens API - Investor Edition v1.0

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
import datetime

app = FastAPI(
    title="Zentra RiskLens API",
    version="1.0 Investor",
    description="Behavioral Financial Infrastructure Layer"
)

VALID_API_KEYS = {
    "zentra-demo-key",
    "zentra-partner-key"
}

# =========================
# MODELS
# =========================

class RiskRequest(BaseModel):
    amount: float
    sector: str = "general"
    sector_risk_level: int = 3
    payment_delay_days: int = 0
    customer_score: int = 70
    exposure_ratio: float = 0.2
    lang: Optional[str] = "en"

class InvoiceRequest(BaseModel):
    invoice_amount: float
    sector: str
    buyer_score: int
    maturity_days: int
    lang: Optional[str] = "en"

# =========================
# HEALTH
# =========================

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "zentra-risklens",
        "version": app.version,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

# =========================
# RISK ENGINE
# =========================

@app.post("/v1/risk")
def calculate_risk(request: RiskRequest, x_api_key: str = Header(None)):

    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    amount_weight = min((request.amount / 50000.0) * 25.0, 25.0)
    sector_weight = (request.sector_risk_level / 5.0) * 20.0
    delay_weight = min((request.payment_delay_days / 60.0) * 25.0, 25.0)
    behavior_weight = ((100.0 - request.customer_score) / 100.0) * 20.0
    exposure_weight = request.exposure_ratio * 10.0

    risk_score = (
        amount_weight +
        sector_weight +
        delay_weight +
        behavior_weight +
        exposure_weight
    )

    if risk_score < 30:
        level = "Low"
    elif risk_score < 60:
        level = "Medium"
    else:
        level = "High"

    response_tr = {
        "risk_score": round(risk_score, 2),
        "risk_level": level,
        "message": "Davranışsal risk skoru hesaplandı."
    }

    response_en = {
        "risk_score": round(risk_score, 2),
        "risk_level": level,
        "message": "Behavioral risk score calculated."
    }

    return {
        "request_id": str(uuid.uuid4()),
        "model": "RiskLens Core",
        "response": response_tr if request.lang == "tr" else response_en,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

# =========================
# INVOICE RISK ENGINE
# =========================

@app.post("/v1/invoice-risk")
def invoice_risk(request: InvoiceRequest, x_api_key: str = Header(None)):

    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    default_probability = max(0.01, (100 - request.buyer_score) / 100)
    liquidity_risk = min(request.maturity_days / 180, 1.0)

    sharia_flag = False
    if request.maturity_days > 365:
        sharia_flag = True

    response_tr = {
        "default_probability": round(default_probability, 2),
        "liquidity_risk_score": round(liquidity_risk, 2),
        "sharia_risk_flag": sharia_flag,
        "message": "Fatura risk analizi tamamlandı."
    }

    response_en = {
        "default_probability": round(default_probability, 2),
        "liquidity_risk_score": round(liquidity_risk, 2),
        "sharia_risk_flag": sharia_flag,
        "message": "Invoice risk analysis completed."
    }

    return {
        "request_id": str(uuid.uuid4()),
        "model": "Invoice Risk Engine",
        "response": response_tr if request.lang == "tr" else response_en,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
