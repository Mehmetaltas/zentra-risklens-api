from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import sqlite3
import datetime

app = FastAPI(title="ZENTRA Core Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


def simulate_business():
    return {
        "cashflow_pressure": 0.6,
        "payment_delay": 0.5,
        "debt_ratio": 0.55
    }

# -----------------------------
# ENGINES
# -----------------------------

def indicator_engine(macro):
    inflation_pressure = min(macro["inflation"] / 10, 1)
    volatility = 0.4
    macro_signal = inflation_pressure * 0.6 + volatility * 0.4
    return {"macro_signal": round(macro_signal, 2)}


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


def behavior_engine(business):
    behavior_score = (
        business["payment_delay"] * 0.6 +
        business["cashflow_pressure"] * 0.4
    )
    return {"behavior_score": round(behavior_score, 2)}


def risk_engine(behavior, economic):
    risk = (
        behavior["behavior_score"] * 0.4 +
        economic["macro_risk"] * 0.4 +
        0.2 * 0.2
    )
    return round(risk * 100, 2)


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


def save_history(risk, global_risk, state):
    timestamp = str(datetime.datetime.utcnow())
    cur.execute("""
    INSERT INTO risk_history(timestamp, risk_score, global_risk, economic_state)
# -----------------------------
# SME INTELLIGENCE ENGINE
# -----------------------------

@app.get("/sme-risk")
def sme_risk():

    sales_pressure = 0.6
    cost_pressure = 0.55
    debt_ratio = 0.5
    payment_delay = 0.4

    score = (
        sales_pressure * 0.3 +
        cost_pressure * 0.25 +
        debt_ratio * 0.25 +
        payment_delay * 0.2
    ) * 100

    if score > 70:
        band = "high"
    elif score > 50:
        band = "medium"
    else:
        band = "low"

    return {
        "sme_risk_score": round(score,2),
        "risk_band": band
    }


# -----------------------------
# BANKING CREDIT ENGINE
# -----------------------------

@app.get("/bank-credit-risk")
def bank_credit():

    customer_score = 65
    delay = 0.3
    sector_risk = 0.5

    risk = (delay*0.4 + sector_risk*0.3 + (1-customer_score/100)*0.3)*100

    return {
        "credit_risk": round(risk,2)
    }


# -----------------------------
# TRADE ENGINE
# -----------------------------

@app.get("/trade-risk")
def trade():

    currency_vol = 0.6
    logistics_risk = 0.4
    demand_pressure = 0.5

    score = (
        currency_vol*0.4 +
        logistics_risk*0.3 +
        demand_pressure*0.3
    )*100

    return {
        "trade_risk_score": round(score,2)
    }


# -----------------------------
# SUPPLY CHAIN ENGINE
# -----------------------------

@app.get("/supply-risk")
def supply():

    raw_material = 0.5
    energy = 0.6
    logistics = 0.4

    score = (
        raw_material*0.35 +
        energy*0.35 +
        logistics*0.3
    )*100

    return {
        "supply_chain_risk": round(score,2)
    }


# -----------------------------
# GLOBAL CRISIS RADAR
# -----------------------------

@app.get("/crisis-radar")
def crisis():

    inflation = 0.6
    market_vol = 0.5
    geopolitical = 0.55

    score = (
        inflation*0.4 +
        market_vol*0.3 +
        geopolitical*0.3
    )*100

    if score > 70:
        level = "high"
    elif score > 50:
        level = "moderate"
    else:
        level = "low"

    return {
        "global_stress_index": round(score,2),
        "crisis_probability": level
    }
