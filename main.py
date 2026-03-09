from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional


app = FastAPI(title="ZENTRA Economic OS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://zentrarisk.com",
        "https://www.zentrarisk.com",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# REQUEST MODELS
# -------------------------

class ChatRequest(BaseModel):
    question: str


class SectorRequest(BaseModel):
    sector: str
    demand: float
    cost_pressure: float
    finance_pressure: float


class SMERequest(BaseModel):
    revenue: float
    cost: float
    debt: float
    delay: int


class SupplyRequest(BaseModel):
    lead_time_days: int
    supplier_risk: float
    logistics_delay_risk: float
    inventory_buffer_days: int


class TradeRequest(BaseModel):
    origin: str
    destination: str
    product: str
    transport_cost: float
    product_price: float


class ScenarioRequest(BaseModel):
    scenario: str


# -------------------------
# HELPERS
# -------------------------

def clamp(value: float, low: float = 0, high: float = 100) -> float:
    return round(max(low, min(high, value)), 2)


def risk_band(score: float) -> str:
    if score >= 80:
        return "critical"
    if score >= 60:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


# -------------------------
# ROOT / HEALTH
# -------------------------

@app.get("/")
def root():
    return {"system": "ZENTRA ECONOMIC OS ACTIVE"}


@app.get("/health")
def health():
    return {"status": "ok"}


# -------------------------
# ECONOMIC BRAIN
# -------------------------

@app.get("/brain")
def brain(country_code: str = Query("TR")):
    country_code = country_code.upper()

    country_profiles = {
        "TR": {
            "inflation": 61.0,
            "policy_rate": 50.0,
            "liquidity": 44.0,
            "volatility": 67.0,
            "energy_stress": 58.0,
        },
        "US": {
            "inflation": 3.4,
            "policy_rate": 5.25,
            "liquidity": 74.0,
            "volatility": 39.0,
            "energy_stress": 36.0,
        },
        "DE": {
            "inflation": 2.8,
            "policy_rate": 4.0,
            "liquidity": 71.0,
            "volatility": 34.0,
            "energy_stress": 41.0,
        },
        "CN": {
            "inflation": 1.4,
            "policy_rate": 3.45,
            "liquidity": 69.0,
            "volatility": 46.0,
            "energy_stress": 44.0,
        },
    }

    p = country_profiles.get(country_code, country_profiles["TR"])

    liquidity_pressure = 100 - p["liquidity"]

    raw_risk = (
        p["inflation"] * 0.60
        + p["policy_rate"] * 0.35
        + liquidity_pressure * 0.30
        + p["volatility"] * 0.25
        + p["energy_stress"] * 0.20
    )

    global_risk_index = clamp(raw_risk)

    if global_risk_index >= 70:
        economic_state = "high pressure"
        market_trend = "bearish"
        advice = "protect liquidity, reduce fragile exposure and keep balance sheet discipline"
    elif global_risk_index >= 45:
        economic_state = "moderate pressure"
        market_trend = "neutral"
        advice = "control cost structure, diversify risk and monitor financing conditions"
    else:
        economic_state = "stable"
        market_trend = "bullish"
        advice = "growth conditions are comparatively supportive, but discipline still matters"

    return {
        "country_code": country_code,
        "global_risk_index": global_risk_index,
        "economic_state": economic_state,
        "market_trend": market_trend,
        "insight": "economic pressure is driven by inflation, rates, liquidity, volatility and energy stress",
        "advice": advice,
        "macro": p,
    }


# -------------------------
# GLOBAL RISK
# -------------------------

@app.get("/global-risk")
def global_risk():
    countries = [
        {"code": "US", "name": "United States", "risk": 44},
        {"code": "DE", "name": "Germany", "risk": 36},
        {"code": "CN", "name": "China", "risk": 48},
        {"code": "IN", "name": "India", "risk": 52},
        {"code": "TR", "name": "Turkey", "risk": 69},
        {"code": "BR", "name": "Brazil", "risk": 55},
        {"code": "NG", "name": "Nigeria", "risk": 73},
        {"code": "AR", "name": "Argentina", "risk": 84},
        {"code": "GB", "name": "United Kingdom", "risk": 43},
        {"code": "JP", "name": "Japan", "risk": 28},
    ]

    for c in countries:
        c["band"] = risk_band(c["risk"])

    return {"countries": countries}


# -------------------------
# CHAT
# -------------------------

@app.post("/chat")
def chat(req: ChatRequest):
    q = req.question.lower()

    if any(x in q for x in ["inflation", "enflasyon"]):
        answer = "Inflation reduces purchasing power, raises cost pressure and usually tightens financial conditions."
    elif any(x in q for x in ["gold", "altın"]):
        answer = "Gold is often used as a defensive asset during inflation and uncertainty, but concentration risk still matters."
    elif any(x in q for x in ["business", "iş", "shop", "dükkan"]):
        answer = "A healthy business needs stable demand, pricing power, cashflow control and manageable debt."
    elif any(x in q for x in ["trade", "ticaret", "logistics", "lojistik"]):
        answer = "Trade profitability depends on margin quality, route efficiency, transport cost and payment reliability."
    elif any(x in q for x in ["recession", "resesyon"]):
        answer = "Recession means weaker demand, slower growth and more pressure on fragile businesses and debt structures."
    else:
        answer = "ZENTRA is analyzing the question within economic context."

    return {
        "question": req.question,
        "answer": answer,
    }


# -------------------------
# SECTOR INTELLIGENCE
# -------------------------

@app.post("/sector-intelligence")
def sector_intelligence(req: SectorRequest):
    sector_base = {
        "agriculture": 42,
        "manufacturing": 55,
        "retail": 58,
        "services": 46,
        "technology": 35,
        "logistics": 50,
        "energy": 57,
        "finance": 48,
        "construction": 62,
    }

    base = sector_base.get(req.sector.lower(), 50)
    demand_pressure = 100 - req.demand

    score = (
        base * 0.35
        + demand_pressure * 0.25
        + req.cost_pressure * 0.20
        + req.finance_pressure * 0.20
    )

    score = clamp(score)
    band = risk_band(score)

    if score >= 70:
        recommendation = "sector is under strong pressure; defensive planning and cash discipline are needed"
    elif score >= 45:
        recommendation = "sector is workable but fragile; monitor demand and margins carefully"
    else:
        recommendation = "sector conditions are comparatively resilient"

    return {
        "sector": req.sector,
        "sector_risk_score": score,
        "band": band,
        "recommendation": recommendation,
    }


# -------------------------
# SME INTELLIGENCE
# -------------------------

@app.post("/sme-intelligence")
def sme_intelligence(req: SMERequest):
    profit = req.revenue - req.cost - req.debt

    risk_score = 35.0
    if profit < 0:
        risk_score += 30
    elif profit < 2000:
        risk_score += 15

    risk_score += req.delay * 0.5
    risk_score = clamp(risk_score)

    return {
        "profit": round(profit, 2),
        "risk_score": risk_score,
        "band": risk_band(risk_score),
    }


# -------------------------
# SUPPLY CHAIN
# -------------------------

@app.post("/supply-chain")
def supply_chain(req: SupplyRequest):
    score = (
        req.lead_time_days * 0.40
        + req.supplier_risk * 0.30
        + req.logistics_delay_risk * 0.20
        - req.inventory_buffer_days * 0.20
    )

    score = clamp(score)

    if score >= 70:
        recommendation = "increase inventory buffer and diversify suppliers"
    elif score >= 40:
        recommendation = "monitor lead times and supplier dependency"
    else:
        recommendation = "supply structure appears comparatively stable"

    return {
        "risk_score": score,
        "band": risk_band(score),
        "recommendation": recommendation,
    }


# -------------------------
# TRADE INTELLIGENCE
# -------------------------

@app.post("/trade-intelligence")
def trade_intelligence(req: TradeRequest):
    margin = req.product_price - req.transport_cost

    if margin > 50:
        viability = "high"
    elif margin > 20:
        viability = "medium"
    else:
        viability = "low"

    return {
        "route": f"{req.origin} → {req.destination}",
        "product": req.product,
        "margin": round(margin, 2),
        "trade_viability": viability,
    }


# -------------------------
# NETWORK
# -------------------------

@app.get("/network")
def network():
    return {
        "supplier_nodes": 120,
        "trade_nodes": 85,
        "logistics_nodes": 42,
        "market_nodes": 64,
        "network_stress": 48,
    }


# -------------------------
# KNOWLEDGE
# -------------------------

@app.get("/knowledge")
def knowledge(topic: str):
    topic = topic.lower()

    if topic == "inflation":
        return {"definition": "Inflation is the rate at which prices rise over time and purchasing power falls."}
    if topic == "cds":
        return {"definition": "CDS is a market-based measure of sovereign or credit default risk."}
    if topic == "recession":
        return {"definition": "Recession is a period of economic slowdown with weaker demand and lower confidence."}

    return {"definition": "economic knowledge topic"}


# -------------------------
# SCENARIO
# -------------------------

@app.post("/scenario")
def scenario(req: ScenarioRequest):
    base = 55.0

    if req.scenario == "interest_shock":
        impact = "credit contraction"
        projected_risk = base + 12
    elif req.scenario == "currency_shock":
        impact = "import inflation"
        projected_risk = base + 15
    elif req.scenario == "oil_shock":
        impact = "energy cost spike"
        projected_risk = base + 10
    else:
        impact = "unknown scenario"
        projected_risk = base

    projected_risk = clamp(projected_risk)

    return {
        "scenario": req.scenario,
        "impact": impact,
        "projected_risk": projected_risk,
        "band": risk_band(projected_risk),
        }
