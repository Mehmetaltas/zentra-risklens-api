from fastapi import FastAPI
from pydantic import BaseModel
import requests
import sqlite3
import datetime

app = FastAPI(title="ZENTRA Core Engine V2")

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

    except:

        inflation = 5.0

    return {"inflation": inflation}


def get_market_data():

    try:

        btc = requests.get(
            "https://api.coindesk.com/v1/bpi/currentprice.json",
            timeout=20
        ).json()

        btc_price = float(btc["bpi"]["USD"]["rate"].replace(",", ""))

    except:

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
# AI INSIGHT ENGINE
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

    INSERT INTO risk_history(timestamp,risk_score,global_risk,economic_state)

    VALUES(?,?,?,?)

    """,(timestamp,risk,global_risk,state))

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

# -----------------------------
# COUNTRY DATA
# -----------------------------

def get_country_risk_data():

    raw = [

        {"code": "US","name":"United States","inflation":42,"interest":48,"currency_vol":30,"debt_stress":55,"political_risk":35},

        {"code": "DE","name":"Germany","inflation":45,"interest":40,"currency_vol":25,"debt_stress":42,"political_risk":20},

        {"code": "CN","name":"China","inflation":35,"interest":38,"currency_vol":40,"debt_stress":50,"political_risk":35},

        {"code": "IN","name":"India","inflation":50,"interest":45,"currency_vol":42,"debt_stress":48,"political_risk":32},

        {"code": "TR","name":"Turkey","inflation":78,"interest":75,"currency_vol":72,"debt_stress":55,"political_risk":45},

        {"code": "BR","name":"Brazil","inflation":55,"interest":52,"currency_vol":58,"debt_stress":50,"political_risk":38},

        {"code": "NG","name":"Nigeria","inflation":72,"interest":60,"currency_vol":75,"debt_stress":58,"political_risk":50},

        {"code": "AR","name":"Argentina","inflation":85,"interest":78,"currency_vol":82,"debt_stress":70,"political_risk":55}

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
# REQUEST MODELS
# -----------------------------

class ScenarioRequest(BaseModel):

    scenario: str


class SectorRequest(BaseModel):

    sector: str
    sales_trend: float
    cost_pressure: float
    demand_index: float

# -----------------------------
# ROOT
# -----------------------------

@app.get("/")
def root():

    return {"system":"ZENTRA CORE ENGINE ACTIVE"}

# -----------------------------
# RISK
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

    risk_score = risk_engine(behavior,economic)

    insight = ai_insight(risk_score)

    return {

        "macro": macro,
        "market": market_state,
        "behavior": behavior,
        "risk_score": risk_score,
        "ai_insight": insight

    }

# -----------------------------
# GLOBAL RISK
# -----------------------------

@app.get("/global-risk")
def global_risk():

    countries = get_country_risk_data()

    return {"countries":countries}

# -----------------------------
# HISTORY
# -----------------------------

@app.get("/history")
def history():

    cur.execute("""

    SELECT timestamp,risk_score,global_risk,economic_state
    FROM risk_history
    ORDER BY id DESC
    LIMIT 20

    """)

    rows = cur.fetchall()

    data=[]

    for r in rows:

        data.append({

            "timestamp":r[0],
            "risk_score":r[1],
            "global_risk":r[2],
            "economic_state":r[3]

        })

    return data
