from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI(title="ZENTRA ECONOMIC OS V4")

# -----------------------------
# REQUEST MODELS
# -----------------------------

class ChatRequest(BaseModel):
    question: str

class BusinessRequest(BaseModel):
    cost: float
    revenue: float

class TradeRequest(BaseModel):
    quantity: float
    unit_cost: float
    unit_price: float
    distance: float

class ScenarioRequest(BaseModel):
    scenario: str

class SupplyChainRequest(BaseModel):
    lead_time_days: float
    supplier_risk: float
    logistics_delay_risk: float
    inventory_buffer_days: float

class SectorRequest(BaseModel):
    sector: str
    demand: float
    cost_pressure: float
    finance_pressure: float

# -----------------------------
# DATA PIPELINE
# -----------------------------

def macro_data():
    inflation = random.uniform(3, 9)
    interest = random.uniform(2, 8)
    liquidity = random.uniform(30, 85)
    volatility = random.uniform(20, 80)
    energy = random.uniform(30, 90)

    return {
        "inflation": round(inflation, 2),
        "interest": round(interest, 2),
        "liquidity": round(liquidity, 2),
        "volatility": round(volatility, 2),
        "energy": round(energy, 2),
    }

# -----------------------------
# ECONOMIC BRAIN
# -----------------------------

def economic_brain():
    data = macro_data()

    liquidity_pressure = 100 - data["liquidity"]

    risk = (
        data["inflation"] * 6 +
        data["interest"] * 4 +
        liquidity_pressure * 0.35 +
        data["volatility"] * 0.25 +
        data["energy"] * 0.15
    ) / 2

    risk = round(min(max(risk, 0), 100), 2)

    if risk > 70:
        state = "high pressure"
        advice = "reduce leverage and protect liquidity"
    elif risk > 45:
        state = "moderate pressure"
        advice = "diversify assets and control costs"
    else:
        state = "stable"
        advice = "growth opportunities available"

    return {
        "macro": data,
        "global_risk_index": risk,
        "economic_state": state,
        "market_trend": market_trend_from_data(data),
        "insight": "macro financial pressure analysis",
        "advice": advice,
    }

def market_trend_from_data(data: dict) -> str:
    v = data["volatility"]
    if v >= 65:
        return "bearish"
    if v >= 40:
        return "neutral"
    return "bullish"

# -----------------------------
# GLOBAL RISK ENGINE
# -----------------------------

def global_risk():
    countries = [
        {"name": "United States", "risk": 44},
        {"name": "Germany", "risk": 36},
        {"name": "China", "risk": 48},
        {"name": "India", "risk": 52},
        {"name": "Turkey", "risk": 68},
        {"name": "Brazil", "risk": 56},
        {"name": "Nigeria", "risk": 73},
        {"name": "Argentina", "risk": 84},
        {"name": "United Kingdom", "risk": 43},
        {"name": "Japan", "risk": 28},
    ]

    for c in countries:
        c["band"] = risk_band(c["risk"])

    return countries

def risk_band(score: float) -> str:
    if score >= 80:
        return "critical"
    if score >= 60:
        return "high"
    if score >= 40:
        return "medium"
    return "low"

# -----------------------------
# SCENARIO ENGINE
# -----------------------------

def scenario_engine(s: str):
    base = random.uniform(40, 70)

    if s == "interest_shock":
        impact = "credit contraction"
        risk = base + 12
    elif s == "currency_shock":
        impact = "import inflation"
        risk = base + 15
    elif s == "oil_shock":
        impact = "energy cost spike"
        risk = base + 10
    elif s == "demand_drop":
        impact = "weaker sales and lower cashflow"
        risk = base + 8
    else:
        impact = "unknown scenario"
        risk = base

    risk = round(min(risk, 100), 2)

    return {
        "scenario": s,
        "impact": impact,
        "projected_risk": risk,
        "band": risk_band(risk),
    }

# -----------------------------
# BUSINESS ENGINE
# -----------------------------

def business_engine(cost: float, revenue: float):
    profit = revenue - cost
    margin = 0 if revenue == 0 else (profit / revenue) * 100

    if profit < 0:
        risk = "high"
        advice = "business losing money"
    elif margin < 20:
        risk = "medium"
        advice = "margin fragile"
    else:
        risk = "low"
        advice = "model sustainable"

    return {
        "profit": round(profit, 2),
        "margin": round(margin, 2),
        "risk": risk,
        "recommendation": advice,
    }

# -----------------------------
# TRADE ENGINE
# -----------------------------

def trade_engine(q: float, c: float, p: float, d: float):
    logistics = q * d * 0.7
    goods = q * c
    total = goods + logistics
    revenue = q * p
    profit = revenue - total
    margin = 0 if revenue == 0 else (profit / revenue) * 100

    risk = "low"
    if profit < 0:
        risk = "high"
    elif margin < 15:
        risk = "medium"

    return {
        "logistics_cost": round(logistics, 2),
        "goods_cost": round(goods, 2),
        "total_cost": round(total, 2),
        "revenue": round(revenue, 2),
        "profit": round(profit, 2),
        "margin": round(margin, 2),
        "risk": risk,
    }

# -----------------------------
# SUPPLY CHAIN ENGINE
# -----------------------------

def supply_chain_engine(
    lead_time_days: float,
    supplier_risk: float,
    logistics_delay_risk: float,
    inventory_buffer_days: float
):
    lead_time_score = min((lead_time_days / 30) * 100, 100)
    buffer_pressure = max(0, 100 - (inventory_buffer_days / 30) * 100)

    risk_score = (
        lead_time_score * 0.25 +
        supplier_risk * 0.30 +
        logistics_delay_risk * 0.25 +
        buffer_pressure * 0.20
    )

    risk_score = round(min(max(risk_score, 0), 100), 2)

    if risk_score >= 70:
        advice = "increase inventory buffer and diversify suppliers"
    elif risk_score >= 40:
        advice = "monitor supplier concentration and delivery timing"
    else:
        advice = "supply chain structure appears stable"

    return {
        "risk_score": risk_score,
        "band": risk_band(risk_score),
        "recommendation": advice,
    }

# -----------------------------
# CRISIS RADAR
# -----------------------------

def crisis_radar():
    brain = economic_brain()
    macro = brain["macro"]

    inflation_pressure = min(macro["inflation"] * 10, 100)
    liquidity_stress = 100 - macro["liquidity"]
    market_fragility = macro["volatility"]
    energy_stress = macro["energy"]

    crisis_score = (
        inflation_pressure * 0.25 +
        liquidity_stress * 0.30 +
        market_fragility * 0.25 +
        energy_stress * 0.20
    )

    crisis_score = round(min(max(crisis_score, 0), 100), 2)

    if crisis_score >= 75:
        signal = "critical"
        message = "crisis probability elevated across macro and market structure"
    elif crisis_score >= 50:
        signal = "stress"
        message = "financial stress building across the system"
    else:
        signal = "watch"
        message = "system should be monitored but remains manageable"

    return {
        "crisis_score": crisis_score,
        "signal": signal,
        "message": message,
        "components": {
            "inflation_pressure": round(inflation_pressure, 2),
            "liquidity_stress": round(liquidity_stress, 2),
            "market_fragility": round(market_fragility, 2),
            "energy_stress": round(energy_stress, 2),
        }
    }

# -----------------------------
# SECTOR INTELLIGENCE
# -----------------------------

def sector_intelligence(sector: str, demand: float, cost_pressure: float, finance_pressure: float):
    sector_base = {
        "agriculture": 42,
        "manufacturing": 55,
        "retail": 58,
        "services": 46,
        "technology": 35,
        "logistics": 50,
        "energy": 57,
        "real_estate": 62,
        "finance": 48,
    }

    base = sector_base.get(sector.lower(), 50)
    demand_pressure = 100 - demand

    score = (
        base * 0.35 +
        demand_pressure * 0.25 +
        cost_pressure * 0.20 +
        finance_pressure * 0.20
    )

    score = round(min(max(score, 0), 100), 2)

    if score >= 70:
        recommendation = "sector under strong pressure; defensive planning needed"
    elif score >= 45:
        recommendation = "sector is workable but fragile; margin discipline matters"
    else:
        recommendation = "sector conditions appear comparatively resilient"

    return {
        "sector": sector,
        "sector_risk_score": score,
        "band": risk_band(score),
        "recommendation": recommendation,
    }

# -----------------------------
# CHAT ENGINE
# -----------------------------

def chat_engine(q: str):
    q = q.lower()

    if "gold" in q:
        return "Gold often performs relatively well during inflation and uncertainty."
    if "economy" in q or "ekonomi" in q:
        return "Economic conditions depend on inflation, interest rates, liquidity and confidence."
    if "business" in q or "iş" in q:
        return "A strong business requires stable demand, good margins and resilient cashflow."
    if "trade" in q or "ticaret" in q:
        return "Trade profitability depends on price discipline, margin and logistics efficiency."
    if "recession" in q or "resesyon" in q:
        return "Recession means weaker demand, slower growth and rising pressure on fragile businesses."

    return "ZENTRA AI is analyzing the question within economic context."

# -----------------------------
# DASHBOARD
# -----------------------------

def dashboard():
    return {
        "brain": economic_brain(),
        "global_risk": global_risk(),
        "crisis_radar": crisis_radar(),
    }

# -----------------------------
# API
# -----------------------------

@app.get("/")
def root():
    return {"system": "ZENTRA ECONOMIC OS ACTIVE"}

@app.get("/brain")
def brain():
    return economic_brain()

@app.get("/global-risk")
def risk():
    return {"countries": global_risk()}

@app.get("/crisis-radar")
def crisis():
    return crisis_radar()

@app.get("/dashboard")
def dashboard_endpoint():
    return dashboard()

@app.post("/chat")
def chat(req: ChatRequest):
    return {
        "question": req.question,
        "answer": chat_engine(req.question)
    }

@app.post("/business")
def business(req: BusinessRequest):
    return business_engine(req.cost, req.revenue)

@app.post("/trade")
def trade(req: TradeRequest):
    return trade_engine(
        req.quantity,
        req.unit_cost,
        req.unit_price,
        req.distance
    )

@app.post("/scenario")
def scenario(req: ScenarioRequest):
    return scenario_engine(req.scenario)

@app.post("/supply-chain")
def supply_chain(req: SupplyChainRequest):
    return supply_chain_engine(
        req.lead_time_days,
        req.supplier_risk,
        req.logistics_delay_risk,
        req.inventory_buffer_days
    )

@app.post("/sector-intelligence")
def sector(req: SectorRequest):
    return sector_intelligence(
        req.sector,
        req.demand,
        req.cost_pressure,
        req.finance_pressure
    )
