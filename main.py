from fastapi import FastAPI
from pydantic import BaseModel
import requests
import sqlite3
import datetime

app = FastAPI(title="ZENTRA Core Engine V3")

# -----------------------------
# DATABASE
# -----------------------------

conn = sqlite3.connect("zentra.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS risk_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    risk_score REAL,
    global_risk REAL,
    economic_state TEXT
)
""")

conn.commit()

# -----------------------------
# REQUEST MODELS
# -----------------------------

class ScenarioRequest(BaseModel):
    scenario: str


class SectorRequest(BaseModel):
    sector: str
    sales_trend: float = 0.5
    cost_pressure: float = 0.5
    demand_index: float = 0.5


class AdvisorRequest(BaseModel):
    question: str


# -----------------------------
# DATA SOURCES
# -----------------------------

def get_macro_data():
    try:
        r = requests.get(
            "https://api.worldbank.org/v2/country/US/indicator/FP.CPI.TOTL.ZG?format=json",
            timeout=20
        )
        data = r.json()
        inflation = float(data[1][0]["value"])
    except Exception:
        inflation = 5.0

    return {"inflation": inflation}


def get_market_data():
    try:
        btc = requests.get(
            "https://api.coindesk.com/v1/bpi/currentprice.json",
            timeout=20
        ).json()
        btc_price = float(btc["bpi"]["USD"]["rate"].replace(",", ""))
    except Exception:
        btc_price = 30000.0

    return {"btc": btc_price}


# -----------------------------
# BUSINESS SIMULATION
# -----------------------------

def simulate_business():
    return {
        "cashflow_pressure": 0.6,
        "payment_delay": 0.5,
        "debt_ratio": 0.55
    }


# -----------------------------
# INDICATOR ENGINE
# -----------------------------

def indicator_engine(macro):
    inflation_pressure = min(macro["inflation"] / 10, 1)
    volatility = 0.4
    macro_signal = inflation_pressure * 0.6 + volatility * 0.4

    return {"macro_signal": round(macro_signal, 2)}


# -----------------------------
# ECONOMIC ENGINE
# -----------------------------

def economic_engine(indicators):
    macro_risk = indicators["macro_signal"]

    if macro_risk > 0.7:
        state = "high pressure"
    elif macro_risk > 0.4:
        state = "moderate pressure"
    else:
        state = "stable"

    return {
        "macro_risk": macro_risk,
        "economic_state": state
    }


# -----------------------------
# MARKET ENGINE
# -----------------------------

def market_engine(market):
    btc = market["btc"]

    if btc > 70000:
        trend = "bullish"
    elif btc < 50000:
        trend = "bearish"
    else:
        trend = "neutral"

    return {
        "btc_price": btc,
        "market_trend": trend
    }


# -----------------------------
# BEHAVIOR ENGINE
# -----------------------------

def behavior_engine(business):
    behavior_score = (
        business["payment_delay"] * 0.6 +
        business["cashflow_pressure"] * 0.4
    )
    return {"behavior_score": round(behavior_score, 2)}


# -----------------------------
# RISK ENGINE
# -----------------------------

def risk_engine(behavior, economic):
    risk = (
        behavior["behavior_score"] * 0.4 +
        economic["macro_risk"] * 0.4 +
        0.2 * 0.2
    )
    return round(risk * 100, 2)


# -----------------------------
# GLOBAL RISK INDEX
# -----------------------------

def global_risk_index(economic, market_state, behavior):
    macro_risk = economic["macro_risk"]
    behavior_score = behavior["behavior_score"]

    if market_state["market_trend"] == "bullish":
        market_risk = 0.45
    elif market_state["market_trend"] == "bearish":
        market_risk = 0.75
    else:
        market_risk = 0.55

    total = (
        macro_risk * 0.4 +
        market_risk * 0.3 +
        behavior_score * 0.3
    )

    return round(total * 100, 2)


# -----------------------------
# AI INSIGHT
# -----------------------------

def ai_insight(risk):
    if risk > 75:
        reason = "high financial pressure"
        advice = "reduce debt and increase liquidity"
    elif risk > 50:
        reason = "moderate economic pressure"
        advice = "monitor cashflow and control expenses"
    else:
        reason = "stable economic environment"
        advice = "maintain financial discipline"

    return {
        "reason": reason,
        "advice": advice
    }


# -----------------------------
# SAVE HISTORY
# -----------------------------

def save_history(risk, global_risk, state):
    timestamp = str(datetime.datetime.utcnow())

    cur.execute("""
    INSERT INTO risk_history(timestamp, risk_score, global_risk, economic_state)
    VALUES (?, ?, ?, ?)
    """, (timestamp, risk, global_risk, state))

    conn.commit()


# -----------------------------
# COUNTRY RISK ENGINE
# -----------------------------

def band(score):
    if score >= 80:
        return "critical"
    elif score >= 65:
        return "high"
    elif score >= 45:
        return "medium"
    elif score >= 25:
        return "low"
    return "very low"


def country_risk_score(inflation, interest, currency_vol, debt_stress, political_risk):
    score = (
        0.30 * inflation +
        0.25 * interest +
        0.20 * currency_vol +
        0.15 * debt_stress +
        0.10 * political_risk
    )
    return round(score, 2)


def get_country_risk_data():
    raw = [
        {"code": "US", "name": "United States", "inflation": 42, "interest": 48, "currency_vol": 30, "debt_stress": 55, "political_risk": 35},
        {"code": "DE", "name": "Germany", "inflation": 45, "interest": 40, "currency_vol": 25, "debt_stress": 42, "political_risk": 20},
        {"code": "CN", "name": "China", "inflation": 35, "interest": 38, "currency_vol": 40, "debt_stress": 50, "political_risk": 35},
        {"code": "IN", "name": "India", "inflation": 50, "interest": 45, "currency_vol": 42, "debt_stress": 48, "political_risk": 32},
        {"code": "TR", "name": "Turkey", "inflation": 78, "interest": 75, "currency_vol": 72, "debt_stress": 55, "political_risk": 45},
        {"code": "BR", "name": "Brazil", "inflation": 55, "interest": 52, "currency_vol": 58, "debt_stress": 50, "political_risk": 38},
        {"code": "NG", "name": "Nigeria", "inflation": 72, "interest": 60, "currency_vol": 75, "debt_stress": 58, "political_risk": 50},
        {"code": "AR", "name": "Argentina", "inflation": 85, "interest": 78, "currency_vol": 82, "debt_stress": 70, "political_risk": 55},
        {"code": "GB", "name": "United Kingdom", "inflation": 46, "interest": 44, "currency_vol": 30, "debt_stress": 50, "political_risk": 28},
        {"code": "JP", "name": "Japan", "inflation": 28, "interest": 20, "currency_vol": 18, "debt_stress": 62, "political_risk": 18}
    ]

    result = []

    for c in raw:
        score = country_risk_score(
            c["inflation"],
            c["interest"],
            c["currency_vol"],
            c["debt_stress"],
            c["political_risk"]
        )

        result.append({
            "code": c["code"],
            "name": c["name"],
            "risk": score,
            "band": band(score)
        })

    return result


# -----------------------------
# SCENARIO ENGINE
# -----------------------------

def scenario_engine(scenario, macro, market, behavior):
    inflation = macro["inflation"]
    behavior_score = behavior["behavior_score"]

    if scenario == "interest_rate_shock":
        macro_risk = min(inflation / 8 + 0.3, 1)
        system_stress = macro_risk * 100
        result = {
            "scenario": "interest_rate_shock",
            "description": "central bank rate increase",
            "impact": "credit contraction and investment slowdown",
            "projected_system_stress": round(system_stress, 2),
            "risk_level": "high"
        }

    elif scenario == "currency_shock":
        macro_risk = min(inflation / 7 + 0.4, 1)
        system_stress = macro_risk * 100
        result = {
            "scenario": "currency_shock",
            "description": "sharp currency depreciation",
            "impact": "import cost increase and inflation pressure",
            "projected_system_stress": round(system_stress, 2),
            "risk_level": "high"
        }

    elif scenario == "oil_price_shock":
        macro_risk = min(inflation / 9 + 0.25, 1)
        system_stress = macro_risk * 100
        result = {
            "scenario": "oil_price_shock",
            "description": "energy price surge",
            "impact": "production cost increase and sector stress",
            "projected_system_stress": round(system_stress, 2),
            "risk_level": "medium"
        }

    elif scenario == "demand_drop":
        business_pressure = behavior_score + 0.3
        system_stress = business_pressure * 100
        result = {
            "scenario": "demand_drop",
            "description": "consumer demand decline",
            "impact": "sales pressure and liquidity stress",
            "projected_system_stress": round(system_stress, 2),
            "risk_level": "medium"
        }

    elif scenario == "credit_crunch":
        credit_pressure = behavior_score + 0.4
        system_stress = credit_pressure * 100
        result = {
            "scenario": "credit_crunch",
            "description": "credit availability tightening",
            "impact": "financing difficulty for businesses",
            "projected_system_stress": round(system_stress, 2),
            "risk_level": "high"
        }

    else:
        result = {
            "scenario": "unknown",
            "description": "scenario not recognized",
            "impact": "no simulation available",
            "projected_system_stress": 0,
            "risk_level": "unknown"
        }

    return result


# -----------------------------
# SECTOR ENGINE
# -----------------------------

def sector_risk_model(sector, sales_trend, cost_pressure, demand_index, macro_risk):
    sector_base_risk = {
        "agriculture": 0.45,
        "retail": 0.55,
        "construction": 0.65,
        "technology": 0.40,
        "energy": 0.50,
        "finance": 0.48,
        "manufacturing": 0.52,
        "logistics": 0.50
    }

    base = sector_base_risk.get(sector.lower(), 0.50)
    sales_pressure = (1 - sales_trend) * 0.4
    cost_effect = cost_pressure * 0.3
    demand_effect = (1 - demand_index) * 0.3

    risk = base * 0.3 + sales_pressure + cost_effect + demand_effect + macro_risk * 0.3
    risk_score = min(risk * 100, 100)

    if risk_score >= 75:
        risk_band = "critical"
    elif risk_score >= 60:
        risk_band = "high"
    elif risk_score >= 40:
        risk_band = "medium"
    else:
        risk_band = "low"

    return round(risk_score, 2), risk_band


# -----------------------------
# ADVISOR ENGINE
# -----------------------------

def detect_advisor_mode(question: str) -> str:
    q = question.lower()

    investment_words = ["altın", "gold", "dolar", "bitcoin", "borsa", "yatırım", "portföy"]
    business_words = ["iş", "işletme", "dükkan", "fabrika", "satış", "maliyet", "berber", "üretim"]
    country_words = ["türkiye", "turkey", "ülke", "ekonomi", "enflasyon", "faiz"]
    crisis_words = ["kriz", "resesyon", "çöküş", "daralma", "savaş"]
    trade_words = ["nakliye", "tır", "lojistik", "ihracat", "ithalat", "göndereceğim", "göndericem"]

    if any(w in q for w in trade_words):
        return "trade"
    if any(w in q for w in business_words):
        return "business"
    if any(w in q for w in investment_words):
        return "investment"
    if any(w in q for w in crisis_words):
        return "crisis"
    if any(w in q for w in country_words):
        return "country"
    return "general"


def advisor_answer(question: str) -> dict:
    mode = detect_advisor_mode(question)

    macro = get_macro_data()
    market = get_market_data()
    business = simulate_business()

    indicators = indicator_engine(macro)
    economic = economic_engine(indicators)
    market_state = market_engine(market)
    behavior = behavior_engine(business)

    risk_score = risk_engine(behavior, economic)
    global_risk = global_risk_index(economic, market_state, behavior)

    if mode == "investment":
        analysis = (
            "Current environment suggests cautious diversification. "
            "Inflation pressure and market sensitivity mean concentrated positioning may increase risk."
        )
        prescription = (
            "Consider a balanced mix of liquidity, inflation hedge instruments, and lower-risk allocation."
        )

    elif mode == "business":
        analysis = (
            "Business conditions show pressure through cashflow sensitivity, cost pressure and financing risk. "
            "Operational discipline matters more than aggressive expansion."
        )
        prescription = (
            "Protect liquidity, shorten collection cycles, control fixed costs and avoid excessive leverage."
        )

    elif mode == "country":
        analysis = (
            "Country-level economic pressure should be read through inflation, financing conditions, market sentiment and policy direction."
        )
        prescription = (
            "Monitor inflation, interest rates, currency volatility and purchasing power before taking major economic decisions."
        )

    elif mode == "crisis":
        analysis = (
            "Crisis risk usually rises when inflation, financing pressure and weak confidence reinforce each other across the system."
        )
        prescription = (
            "Stay liquid, reduce fragile exposure and focus on resilience rather than short-term speculation."
        )

    elif mode == "trade":
        analysis = (
            "Trade and logistics decisions should combine transport cost, timing, route efficiency and product margin."
        )
        prescription = (
            "Compare shipment cost, delivery time, unit margin and customer payment speed before finalizing the trade."
        )

    else:
        analysis = (
            "The current environment can be interpreted through macro pressure, market trend and business sensitivity together."
        )
        prescription = (
            "Use data, avoid concentrated risk and make step-by-step economic decisions."
        )

    return {
        "mode": mode,
        "question": question,
        "risk_score": risk_score,
        "global_risk_index": global_risk,
        "economic_state": economic["economic_state"],
        "market_trend": market_state["market_trend"],
        "analysis": analysis,
        "prescription": prescription
    }


# -----------------------------
# ROOT
# -----------------------------

@app.get("/")
def root():
    return {"system": "ZENTRA CORE ENGINE ACTIVE"}


# -----------------------------
# RISK ENDPOINT
# -----------------------------

@app.get("/risk")
def risk():
    macro = get_macro_data()
    market = get_market_data()
    business = simulate_business()

    indicators = indicator_engine(macro)
    economic = economic_engine(indicators)
    market_state = market_engine(market)
    behavior = behavior_engine(business)

    risk_score = risk_engine(behavior, economic)
    insight = ai_insight(risk_score)

    return {
        "macro": macro,
        "market": market_state,
        "behavior": behavior,
        "risk_score": risk_score,
        "ai_insight": insight
    }


# -----------------------------
# TELESCOPE ENDPOINT
# -----------------------------

@app.get("/telescope")
def telescope():
    macro = get_macro_data()
    market = get_market_data()
    business = simulate_business()

    indicators = indicator_engine(macro)
    economic = economic_engine(indicators)
    market_state = market_engine(market)
    behavior = behavior_engine(business)

    risk_score = risk_engine(behavior, economic)
    global_risk = global_risk_index(economic, market_state, behavior)
    insight = ai_insight(risk_score)

    save_history(
        risk_score,
        global_risk,
        economic["economic_state"]
    )

    return {
        "macro": macro,
        "market": market_state,
        "risk_score": risk_score,
        "global_risk_index": global_risk,
        "risk_band": band(global_risk),
        "economic_state": economic["economic_state"],
        "ai_reason": insight["reason"],
        "ai_advice": insight["advice"]
    }


# -----------------------------
# HISTORY ENDPOINT
# -----------------------------

@app.get("/history")
def history():
    cur.execute("""
    SELECT timestamp, risk_score, global_risk, economic_state
    FROM risk_history
    ORDER BY id DESC
    LIMIT 20
    """)

    rows = cur.fetchall()
    data = []

    for r in rows:
        data.append({
            "timestamp": r[0],
            "risk_score": r[1],
            "global_risk": r[2],
            "economic_state": r[3]
        })

    return data


# -----------------------------
# GLOBAL RISK ENDPOINT
# -----------------------------

@app.get("/global-risk")
def global_risk():
    countries = get_country_risk_data()
    return {"countries": countries}


# -----------------------------
# SCENARIO ENDPOINT
# -----------------------------

@app.post("/scenario")
def run_scenario(req: ScenarioRequest):
    macro = get_macro_data()
    market = get_market_data()
    business = simulate_business()

    indicators = indicator_engine(macro)
    economic = economic_engine(indicators)
    behavior = behavior_engine(business)

    result = scenario_engine(
        req.scenario,
        macro,
        market,
        behavior
    )

    return {
        "macro_environment": economic["economic_state"],
        "scenario_result": result
    }


# -----------------------------
# SECTOR RISK ENDPOINT
# -----------------------------

@app.post("/sector-risk")
def sector_risk(req: SectorRequest):
    macro = get_macro_data()
    indicators = indicator_engine(macro)
    economic = economic_engine(indicators)
    macro_risk = economic["macro_risk"]

    score, risk_band = sector_risk_model(
        req.sector,
        req.sales_trend,
        req.cost_pressure,
        req.demand_index,
        macro_risk
    )

    return {
        "sector": req.sector,
        "sector_risk_score": score,
        "risk_band": risk_band,
        "macro_environment": economic["economic_state"]
    }


# -----------------------------
# ADVISOR ENDPOINT
# -----------------------------

@app.post("/advisor")
def advisor(req: AdvisorRequest):
    return advisor_answer(req.question)
