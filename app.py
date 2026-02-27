from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"status": "Zentra RiskLens API is live"}


@app.get("/risk")
def calculate_risk(amount: float):
    score = amount * 0.42
    return {
        "amount": amount,
        "risk_score": score
    }
