# Risk Engine v1.1
@app.post("/v1/risk")
def calculate_risk(
    request: RiskRequest,
    x_api_key: str = Header(None)
):

    if x_api_key != API_KEY:
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
