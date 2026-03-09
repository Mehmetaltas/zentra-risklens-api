from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI(title="ZENTRA AI CORE V2")

# -----------------------------
# MODELS
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

# -----------------------------
# DATA PIPELINE (BASE)
# -----------------------------

def data_pipeline():
    inflation = round(random.uniform(3.5, 9.5), 2)
    interest = round(random.uniform(2.0, 8.5), 2)
    liquidity = round(random.uniform(30, 85), 2)
    market_volatility = round(random.uniform(20, 80), 2)
    energy_stress = round(random.uniform(25, 85), 2)

    return {
        "inflation": inflation,
        "interest": interest,
        "liquidity": liquidity,
        "market_volatility": market_volatility,
        "energy_stress": energy_stress,
    }

# -----------------------------
# RISK / BRAIN
# -----------------------------

def calculate_macro_pressure(data: dict) -> float:
    # lower liquidity = higher pressure
    liquidity_pressure = 100 - data["liquidity"]

    pressure = (
        data["inflation"] * 6 +
        data["interest"] * 4 +
        liquidity_pressure * 0.35 +
        data["market_volatility"] * 0.20 +
        data["energy_stress"] * 0.15
    ) / 2.0

    return round(min(max(pressure, 0), 100), 2)

def pressure_state(score: float) -> str:
    if score >= 70:
        return "high pressure"
    if score >= 45:
        return "moderate pressure"
    return "stable"

def market_trend(data: dict) -> str:
    if data["market_volatility"] >= 65:
        return "bearish"
    if data["market_volatility"] >= 40:
        return "neutral"
    return "bullish"

def economic_brain():
    data = data_pipeline()
    pressure = calculate_macro_pressure(data)
    state = pressure_state(pressure)
    trend = market_trend(data)

    if pressure >= 70:
        insight = "systemic financial stress is rising across markets and financing conditions are tightening"
        advice = "protect liquidity, reduce fragile exposure and prioritize resilience"
    elif pressure >= 45:
        insight = "the environment is balanced but fragile, with visible macro pressure and market sensitivity"
        advice = "diversify risk, control costs and avoid concentrated positions"
    else:
        insight = "economic conditions are relatively stable and risk appetite can improve"
        advice = "growth opportunities exist, but maintain disciplined allocation"

    return {
        "macro": data,
        "global_risk_index": pressure,
        "economic_state": state,
        "market_trend": trend,
        "insight": insight,
        "advice": advice,
    }

# -----------------------------
# GLOBAL RISK ENGINE
# -----------------------------

def global_risk_engine():
    countries = [
        {"code": "US", "name": "United States", "risk": 44},
        {"code": "DE", "name": "Germany", "risk": 36},
        {"code": "CN", "name": "China", "risk": 48},
        {"code": "IN", "name": "India", "risk": 52},
        {"code": "TR", "name": "Turkey", "risk": 68},
        {"code": "BR", "name": "Brazil", "risk": 56},
        {"code": "NG", "name": "Nigeria", "risk": 73},
        {"code": "AR", "name": "Argentina", "risk": 84},
        {"code": "GB", "name": "United Kingdom", "risk": 43},
        {"code": "JP", "name": "Japan", "risk": 28},
    ]

    for c in countries:
        if c["risk"] >= 80:
            c["band"] = "critical"
        elif c["risk"] >= 60:
            c["band"] = "high"
        elif c["risk"] >= 40:
            c["band"] = "medium"
        else:
            c["band"] = "low"

    return countries

# -----------------------------
# CHAT ENGINE
# -----------------------------

def chat_engine(question: str) -> str:
    q = question.lower()

    if "gold" in q or "altın" in q:
        return "Gold usually performs better when inflation pressure is high and financial uncertainty increases."

    if "business" in q or "iş" in q or "shop" in q or "dükkan" in q:
        return "A sustainable business depends on stable demand, cost discipline, pricing power and cashflow resilience."

    if "economy" in q or "ekonomi" in q:
        return "Economic conditions should be read through inflation, interest rates, liquidity and market confidence together."

    if "trade" in q or "ticaret" in q or "logistics" in q or "lojistik" in q:
        return "Trade decisions depend on margin strength, transport cost, timing, route efficiency and payment quality."

    if "farm" in q or "çiftlik" in q or "tarım" in q:
        return "Agricultural decisions should combine input cost, water and energy pressure, seasonal demand and transport efficiency."

    return "ZENTRA AI is analyzing your question within a general and economic context."

# -----------------------------
# BUSINESS ENGINE
# -----------------------------

def business_simulation(cost: float, revenue: float):
    profit = revenue - cost
    margin = 0 if revenue == 0 else round((profit / revenue) * 100, 2)

    if profit < 0:
        risk = "high"
        recommendation = "reduce costs, revise pricing and strengthen demand before scaling"
    elif profit < 2000:
        risk = "medium"
        recommendation = "the model works but margin is fragile; improve efficiency and collections"
    else:
        risk = "low"
        recommendation = "the business model looks sustainable if demand remains stable"

    return {
        "profit": round(profit, 2),
        "margin": margin,
        "risk": risk,
        "recommendation": recommendation,
    }

# -----------------------------
# TRADE ENGINE
# -----------------------------

def trade_engine(quantity: float, unit_cost: float, unit_price: float, distance: float):
    logistics_cost = distance * 0.7 * quantity
    goods_cost = quantity * unit_cost
    total_cost = goods_cost + logistics_cost
    revenue = quantity * unit_price
    profit = revenue - total_cost
    margin = 0 if revenue == 0 else round((profit / revenue) * 100, 2)

    if profit < 0:
        risk = "high"
        advice = "route or pricing is weak; reduce transport cost or improve selling price"
    elif margin < 15:
        risk = "medium"
        advice = "margin is limited; protect against fuel, delay and collection risk"
    else:
        risk = "low"
        advice = "trade structure is commercially workable if execution stays disciplined"

    return {
        "logistics_cost": round(logistics_cost, 2),
        "goods_cost": round(goods_cost, 2),
        "total_cost": round(total_cost, 2),
        "revenue": round(revenue, 2),
        "profit": round(profit, 2),
        "margin": margin,
        "risk": risk,
        "advice": advice,
    }

# -----------------------------
# SCENARIO ENGINE
# -----------------------------

def scenario_engine(scenario: str):
    brain = economic_brain()
    base = brain["global_risk_index"]

    s = scenario.lower()

    if s == "interest_shock":
        projected = min(base + 12, 100)
        impact = "credit becomes more expensive and business expansion slows"
    elif s == "oil_shock":
        projected = min(base + 10, 100)
        impact = "energy and logistics costs rise, increasing sector pressure"
    elif s == "currency_shock":
        projected = min(base + 15, 100)
        impact = "import cost rises and inflation pressure intensifies"
    elif s == "demand_drop":
        projected = min(base + 8, 100)
        impact = "sales weaken and cashflow pressure rises across businesses"
    else:
        projected = base
        impact = "scenario not recognized; no additional shock applied"

    return {
        "base_risk": base,
        "projected_risk": round(projected, 2),
        "scenario": s,
        "impact": impact,
        "projected_state": pressure_state(projected),
    }

# -----------------------------
# DASHBOARD ENGINE
# -----------------------------

def dashboard_engine():
    brain = economic_brain()
    countries = global_risk_engine()

    return {
        "brain": brain,
        "countries": countries,
        "summary": {
            "global_risk_index": brain["global_risk_index"],
            "economic_state": brain["economic_state"],
            "market_trend": brain["market_trend"],
            "insight": brain["insight"],
            "advice": brain["advice"],
        }
    }

# -----------------------------
# ENDPOINTS
# -----------------------------

@app.get("/")
def root():
    return {"system": "ZENTRA AI CORE ACTIVE"}

@app.get("/brain")
def brain():
    return economic_brain()

@app.get("/global-risk")
def global_risk():
    return {"countries": global_risk_engine()}

@app.get("/dashboard")
def dashboard():
    return dashboard_engine()

@app.post("/chat")
def chat(req: ChatRequest):
    return {
        "question": req.question,
        "answer": chat_engine(req.question)
    }

@app.post("/business")
def business(req: BusinessRequest):
    return business_simulation(req.cost, req.revenue)

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
