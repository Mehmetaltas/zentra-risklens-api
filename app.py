from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uuid
import datetime

app = FastAPI(
    title="Zentra RiskLens API",
    version="1.1",
    docs_url=None,
    redoc_url=None
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
    sector_risk_level: int
    payment_delay_days: int
    customer_score: int
    exposure_ratio: float

# =========================
# ROOT LANDING PAGE
# =========================

@app.get("/", response_class=HTMLResponse)
def landing():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Zentra RiskLens</title>
        <meta charset="utf-8"/>
        <style>
            body {
                background: #0f172a;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 60px;
            }
            h1 {
                font-size: 42px;
                margin-bottom: 10px;
            }
            p {
                font-size: 18px;
                opacity: 0.8;
            }
            .box {
                margin-top: 40px;
                padding: 25px;
                background: #1e293b;
                border-radius: 12px;
                display: inline-block;
            }
            .badge {
                margin-top: 20px;
                display: inline-block;
                padding: 8px 14px;
                background: #2563eb;
                border-radius: 20px;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <h1>Zentra RiskLens</h1>
        <p>AI-Powered Modular Risk Intelligence Infrastructure</p>

        <div class="box">
            <p><strong>Status:</strong> LIVE</p>
            <p><strong>Version:</strong> 1.1</p>
            <p><strong>Endpoint:</strong> POST /v1/risk</p>
        </div>

        <div class="badge">
            Production Environment Active
        </div>
    </body>
    </html>
    """

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

    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")

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

    if risk_score < 30:
        level = "Low"
    elif risk_score < 60:
        level = "Medium"
    else:
        level = "High"

    return {
        "request_id": str(uuid.uuid4()),
        "model_version": "1.1",
        "risk_score": round(risk_score, 2),
        "risk_level": level,
        "confidence": 0.91,
        "timestamp": datetime.datetime.utcnow()
    }
