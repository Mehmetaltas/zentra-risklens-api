from fastapi import FastAPI
import requests
import statistics

app = FastAPI(title="ZENTRA Core Engine")

# -------------------------------
# DATA SOURCES
# -------------------------------

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

# -------------------------------
# SIMULATION
# -------------------------------

def simulate_business():
    return {
        "cashflow_pressure": 0.6,
        "payment_delay": 0.5,
        "debt_ratio": 0.55
    }

# -------------------------------
# RISK ENGINE
# -------------------------------

def calculate_risk(macro, market, business):

    behavior = (
        business["payment_delay"] * 0.5 +
        business["cashflow_pressure"] * 0.5
    )

    stress = business["debt_ratio"]

    macro_risk = min(macro["inflation"] / 10, 1)

    security = 0.2

    risk = (
        behavior * 0.35 +
        stress * 0.30 +
        macro_risk * 0.20 +
        security * 0.15
    )

    return round(risk * 100, 2)

# -------------------------------
# API
# -------------------------------

@app.get("/")
def root():
    return {"system": "ZENTRA CORE ENGINE"}

@app.get("/risk")
def risk():

    macro = get_macro_data()
    market = get_market_data()
    business = simulate_business()

    score = calculate_risk(macro, market, business)

    return {
        "macro": macro,
        "market": market,
        "business": business,
        "risk_score": score
  }
