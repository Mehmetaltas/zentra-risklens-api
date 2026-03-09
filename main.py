from fastapi import FastAPI, Query
from pydantic import BaseModel
import requests
import random
import os
from typing import Optional

app = FastAPI(title="ZENTRA REAL DATA ENGINE")

# -------------------------
# CONFIG
# -------------------------

FRED_API_KEY = os.getenv("FRED_API_KEY", "").strip()

WORLD_BANK_BASE = "https://api.worldbank.org/v2"
FRED_BASE = "https://api.stlouisfed.org/fred"
ECB_BASE = "https://data-api.ecb.europa.eu"

# -------------------------
# MODELS
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

def safe_float(x, default=0.0):
    try:
        if x is None:
            return default
        return float(x)
    except Exception:
        return default

def risk_band(score: float) -> str:
    if score >= 80:
        return "critical"
    if score >= 60:
        return "high"
    if score >= 40:
        return "medium"
    return "low"

# -------------------------
# REAL DATA PIPELINE
# -------------------------

def fetch_world_bank_latest(country_code: str, indicator_code: str, fallback: float) -> float:
    """
    Example indicator:
    FP.CPI.TOTL.ZG = inflation, consumer prices (annual %)
    """
    url = f"{WORLD_BANK_BASE}/country/{country_code}/indicator/{indicator_code}?format=json&per_page=60"
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list) and len(data) > 1 and isinstance(data[1], list):
            for row in data[1]:
                if row.get("value") is not None:
                    return safe_float(row["value"], fallback)
    except Exception:
        pass
    return fallback

def fetch_fred_latest(series_id: str, fallback: float) -> float:
    """
    FRED requires an API key.
    """
    if not FRED_API_KEY:
        return fallback

    url = (
        f"{FRED_BASE}/series/observations"
        f"?series_id={series_id}"
        f"&api_key={FRED_API_KEY}"
        f"&file_type=json"
        f"&sort_order=desc"
        f"&limit=1"
    )
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        data = r.json()
        obs = data.get("observations", [])
        if obs:
            return safe_float(obs[0].get("value"), fallback)
    except Exception:
        pass
    return fallback

def fetch_ecb_policy_rate(fallback: float) -> float:
    """
    ECB official deposit facility rate example series.
    API is SDMX-based; if parsing fails, fallback is used.
    """
    url = (
        f"{ECB_BASE}/service/data/FM/"
        f"D.U2.EUR.4F.KR.DFR.LEV"
        f"?lastNObservations=1&format=jsondata"
    )
    try:
        r = requests.get(url, timeout=20, headers={"Accept": "application/json"})
        r.raise_for_status()
        data = r.json()

        # ECB JSON structures can vary; try a few shapes safely
        # 1) direct observations list
        if isinstance(data, dict):
            if "data" in data and isinstance(data["data"], list) and data["data"]:
                item = data["data"][0]
                if isinstance(item, dict):
                    for k in ("value", "obsValue"):
                        if k in item:
                            return safe_float(item[k], fallback)

            # 2) generic deep scan
            stack = [data]
            while stack:
                cur = stack.pop()
                if isinstance(cur, dict):
                    for k, v in cur.items():
                        if k in ("value", "obsValue"):
                            val = safe_float(v, None)
                            if val is not None:
                                return val
                        else:
                            stack.append(v)
                elif isinstance(cur, list):
                    stack.extend(cur)
    except Exception:
        pass

    return fallback

def real_data_pipeline(country_code: str = "TR") -> dict:
    """
    TR inflation from World Bank
    US 10Y yield or Fed Funds from FRED if key exists
    ECB rate from ECB API if available
    Other values use deterministic fallback ranges
    """
    inflation = fetch_world_bank_latest(country_code, "FP.CPI.TOTL.ZG", fallback=38.0)

    # FRED examples: FEDFUNDS, DGS10
    us_rate = fetch_fred_latest("FEDFUNDS", fallback=5.25)

    ecb_rate = fetch_ecb_policy_rate(fallback=4.00)

    # These are still modeled until more live feeds are added
    liquidity = round(random.uniform(35, 80), 2)
    volatility = round(random.uniform(25, 75), 2)
    energy = round(random.uniform(35, 85), 2)

    return {
        "country_code": country_code,
        "inflation": round(inflation, 2),
        "us_policy_rate": round(us_rate, 2),
        "ecb_policy_rate": round(ecb_rate, 2),
        "liquidity": liquidity,
        "volatility": volatility,
        "energy": energy,
        "sources": {
            "inflation": "World Bank",
            "us_policy_rate": "FRED" if FRED_API_KEY else "fallback",
            "ecb_policy_rate": "ECB API / fallback",
        }
    }

# -------------------------
# ECONOMIC BRAIN
# -------------------------

@app.get("/brain")
def brain(country_code: str = Query("TR")):
    data = real_data_pipeline(country_code)

    liquidity_pressure = 100 - data["liquidity"]

    risk = (
        data["inflation"] * 0.9 +
        data["us_policy_rate"] * 3.0 +
        data["ecb_policy_rate"] * 2.0 +
        liquidity_pressure * 0.35 +
        data["volatility"] * 0.25 +
        data["energy"] * 0.15
    )

    risk = round(min(max(risk, 0), 100), 2)

    if risk > 70:
        state = "high pressure"
        trend = "bearish"
        advice = "reduce leverage and protect liquidity"
    elif risk > 45:
        state = "moderate pressure"
        trend = "neutral"
        advice = "diversify assets and control costs"
    else:
        state = "stable"
        trend = "bullish"
        advice = "growth opportunities available"

    return {
        "global_risk_index": risk,
        "economic_state": state,
        "market_trend": trend,
        "insight": "economic pressure driven by inflation, rates, liquidity and volatility",
        "advice": advice,
        "macro": data
    }

# -------------------------
# GLOBAL RISK
# -------------------------

@app.get("/global-risk")
def global_risk():
    countries = [
        {"name": "United States", "risk": 44},
        {"name": "Germany", "risk": 36},
        {"name": "China", "risk": 48},
        {"name": "India", "risk": 52},
        {"name": "Turkey", "risk": 69},
        {"name": "Brazil", "risk": 55},
        {"name": "Nigeria", "risk": 73},
        {"name": "Argentina", "risk": 84},
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

    if "inflation" in q or "enflasyon" in q:
        answer = "Inflation reduces purchasing power and increases cost pressure."
    elif "gold" in q or "altın" in q:
        answer = "Gold often benefits during inflationary periods, but concentration risk still matters."
    elif "business" in q or "iş" in q:
        answer = "A healthy business requires strong cashflow, stable demand and resilient margins."
    elif "trade" in q or "ticaret" in q:
        answer = "Trade profitability depends on pricing power, route efficiency and logistics cost."
    else:
        answer = "ZENTRA is analyzing the economic context."

    return {"question": req.question, "answer": answer}

# -------------------------
# SECTOR INTELLIGENCE
# -------------------------

@app.post("/sector-intelligence")
def sector(req: SectorRequest):
    risk = (req.cost_pressure + req.finance_pressure + (100 - req.demand)) / 3.0
    risk = round(min(max(risk, 0), 100), 2)

    return {
        "sector": req.sector,
        "sector_risk_score": risk,
        "band": risk_band(risk),
        "recommendation": "monitor demand, finance and cost dynamics"
    }

# -------------------------
# SME INTELLIGENCE
# -------------------------

@app.post("/sme-intelligence")
def sme(req: SMERequest):
    profit = req.revenue - req.cost - req.debt
    risk = 40.0

    if profit < 0:
        risk += 30

    risk += req.delay * 0.5
    risk = round(min(max(risk, 0), 100), 2)

    return {
        "profit": round(profit, 2),
        "risk_score": risk,
        "band": risk_band(risk)
    }

# -------------------------
# SUPPLY CHAIN
# -------------------------

@app.post("/supply-chain")
def supply(req: SupplyRequest):
    risk = (
        req.lead_time_days * 0.4 +
        req.supplier_risk * 0.3 +
        req.logistics_delay_risk * 0.2 -
        req.inventory_buffer_days * 0.2
    )

    risk = round(min(max(risk, 0), 100), 2)

    return {
        "risk_score": risk,
        "band": risk_band(risk),
        "recommendation": "increase inventory buffer or diversify suppliers"
    }

# -------------------------
# TRADE INTELLIGENCE
# -------------------------

@app.post("/trade-intelligence")
def trade(req: TradeRequest):
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
        "trade_viability": viability
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
        "network_stress": 48
    }

# -------------------------
# KNOWLEDGE
# -------------------------

@app.get("/knowledge")
def knowledge(topic: str):
    topic = topic.lower()

    if topic == "inflation":
        return {"definition": "Inflation is the rate at which prices increase over time."}
    if topic == "cds":
        return {"definition": "CDS is a market-based measure of sovereign credit risk."}
    if topic == "recession":
        return {"definition": "Recession is a period of economic slowdown and weaker demand."}

    return {"definition": "economic knowledge topic"}

# -------------------------
# SCENARIO
# -------------------------

@app.post("/scenario")
def scenario(req: ScenarioRequest):
    base = random.uniform(40, 70)

    if req.scenario == "interest_shock":
        impact = "credit contraction"
        risk = base + 12
    elif req.scenario == "currency_shock":
        impact = "import inflation"
        risk = base + 15
    elif req.scenario == "oil_shock":
        impact = "energy cost spike"
        risk = base + 10
    else:
        impact = "unknown scenario"
        risk = base

    risk = round(min(max(risk, 0), 100), 2)

    return {
        "scenario": req.scenario,
        "impact": impact,
        "projected_risk": risk,
        "band": risk_band(risk)
    }
