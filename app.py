from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="Zentra RiskLens API",
    description="AI-powered modular credit risk infrastructure for modern finance platforms.",
    version="1.1"
)

API_KEY = "zentra-secure-key"


class RiskInput(BaseModel):
    income: float
    debt: float
    transaction_amount: float
    credit_score: int


@app.get("/")
def root():
    return {"status": "Zentra RiskLens API is live"}


@app.post("/risk")
def calculate_risk(data: RiskInput, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    debt_ratio = data.debt / data.income
    exposure = data.transaction_amount / data.income

    score = (
        debt_ratio * 40 +
        exposure * 30 +
        (700 - data.credit_score) * 0.05
    )

    risk_level = (
        "LOW" if score < 30 else
        "MEDIUM" if score < 60 else
        "HIGH"
    )

    return {
        "model_version": "1.1",
        "risk_score": round(score, 2),
        "risk_level": risk_level,
        "confidence": 0.87,
        "timestamp": datetime.utcnow().isoformat()
    }
