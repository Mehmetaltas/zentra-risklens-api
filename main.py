from fastapi import FastAPI
import requests

app = FastAPI(title="ZENTRA Core Engine")

# -----------------------------
# DATA SOURCES
# -----------------------------

def get_macro_data():
    try:
        r = requests.get(
            "https://api.worldbank.org/v2/country/US/indicator/FP.CPI.TOTL.ZG?format=json"
        )
        data = r.json()
        inflation = float(data[1][0]["value"])
    except:
        inflation = 5

    return {
        "inflation": inflation
    }

def get_market_data():
    try:
        btc = requests.get(
            "https://api.coindesk.com/v1/bpi/currentprice.json"
        ).json()

        btc_price = float(btc["bpi"]["USD"]["rate"].replace(",", ""))
    except:
        btc_price = 30000

    return {
        "btc": btc_price
    }

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
# 1 INDICATOR ENGINE
# -----------------------------

def indicator_engine(macro, market):

    inflation_pressure = min(macro["inflation"] / 10, 1)

    volatility = 0.4

    macro_signal = (
        inflation_pressure * 0.6 +
        volatility * 0.4
    )

    return {
        "inflation_pressure": inflation_pressure,
        "volatility": volatility,
        "macro_signal": round(macro_signal, 2)
    }

# -----------------------------
# 2 ECONOMIC ENGINE
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
# 3 MARKET ENGINE
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
# 4 BEHAVIOR ENGINE
# -----------------------------

def behavior_engine(business):

    payment_risk = business["payment_delay"]

    cashflow_risk = business["cashflow_pressure"]

    behavior_score = (
        payment_risk * 0.6 +
        cashflow_risk * 0.4
    )

    return {
        "behavior_score": round(behavior_score, 2)
    }

# -----------------------------
# 5 RISK ENGINE
# -----------------------------

def risk_engine(behavior, economic):

    behavior_score = behavior["behavior_score"]

    macro_risk = economic["macro_risk"]

    security = 0.2

    risk = (
        behavior_score * 0.4 +
        macro_risk * 0.4 +
        security * 0.2
    )

    return round(risk * 100, 2)

# -----------------------------
# 6 STRATEGY ENGINE
# -----------------------------

def strategy_engine(risk):

    if risk > 75:
        action = "reduce debt and increase liquidity"

    elif risk > 50:
        action = "monitor cashflow and control expenses"

    else:
        action = "stable condition"

    return {
        "strategy": action
    }

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
# RISK BAND
# -----------------------------

def risk_band(score):

    if score >= 80:
        return "critical"

    elif score >= 60:
        return "high"

    elif score >= 40:
        return "medium"

    elif score >= 20:
        return "low"

    return "very low"

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

    indicators = indicator_engine(macro, market)

    economic = economic_engine(indicators)

    market_state = market_engine(market)

    behavior = behavior_engine(business)

    risk_score = risk_engine(behavior, economic)

    strategy = strategy_engine(risk_score)

    return {
        "macro": macro,
        "market": market_state,
        "business": business,
        "indicators": indicators,
        "economic": economic,
        "behavior": behavior,
        "risk_score": risk_score,
        "strategy": strategy
    }

# -----------------------------
# TELESCOPE ENDPOINT
# -----------------------------

@app.get("/telescope")
def telescope():

    macro = get_macro_data()

    market = get_market_data()

    business = simulate_business()

    indicators = indicator_engine(macro, market)

    economic = economic_engine(indicators)

    market_state = market_engine(market)

    behavior = behavior_engine(business)

    risk_score = risk_engine(behavior, economic)

    strategy = strategy_engine(risk_score)

    global_score = global_risk_index(
        economic,
        market_state,
        behavior
    )

    band = risk_band(global_score)

    return {
        "macro": macro,
        "market": market_state,
        "behavior": behavior,
        "risk_score": risk_score,
        "global_risk_index": global_score,
        "risk_band": band,
        "economic_state": economic["economic_state"],
        "strategy": strategy
    }
