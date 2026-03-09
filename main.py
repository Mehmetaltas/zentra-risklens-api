from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI(title="ZENTRA ECONOMIC OS")

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

# -----------------------------
# DATA PIPELINE
# -----------------------------

def macro_data():

    inflation = random.uniform(3,9)
    interest = random.uniform(2,8)
    liquidity = random.uniform(30,85)
    volatility = random.uniform(20,80)
    energy = random.uniform(30,90)

    return {
        "inflation":round(inflation,2),
        "interest":round(interest,2),
        "liquidity":round(liquidity,2),
        "volatility":round(volatility,2),
        "energy":round(energy,2)
    }

# -----------------------------
# ECONOMIC BRAIN
# -----------------------------

def economic_brain():

    data = macro_data()

    liquidity_pressure = 100-data["liquidity"]

    risk = (
        data["inflation"]*6+
        data["interest"]*4+
        liquidity_pressure*0.35+
        data["volatility"]*0.25+
        data["energy"]*0.15
    )/2

    risk = round(min(max(risk,0),100),2)

    if risk>70:
        state="high pressure"
        advice="reduce leverage and protect liquidity"

    elif risk>45:
        state="moderate pressure"
        advice="diversify assets and control costs"

    else:
        state="stable"
        advice="growth opportunities available"

    return {
        "macro":data,
        "global_risk_index":risk,
        "economic_state":state,
        "market_trend":"neutral",
        "insight":"macro financial pressure analysis",
        "advice":advice
    }

# -----------------------------
# GLOBAL RISK ENGINE
# -----------------------------

def global_risk():

    countries=[

        {"name":"United States","risk":44},
        {"name":"Germany","risk":36},
        {"name":"China","risk":48},
        {"name":"India","risk":52},
        {"name":"Turkey","risk":68},
        {"name":"Brazil","risk":56},
        {"name":"Nigeria","risk":73},
        {"name":"Argentina","risk":84},
        {"name":"United Kingdom","risk":43},
        {"name":"Japan","risk":28}

    ]

    for c in countries:

        if c["risk"]>=80:
            c["band"]="critical"

        elif c["risk"]>=60:
            c["band"]="high"

        elif c["risk"]>=40:
            c["band"]="medium"

        else:
            c["band"]="low"

    return countries

# -----------------------------
# SCENARIO ENGINE
# -----------------------------

def scenario_engine(s):

    base=random.uniform(40,70)

    if s=="interest_shock":

        impact="credit contraction"
        risk=base+12

    elif s=="currency_shock":

        impact="import inflation"
        risk=base+15

    elif s=="oil_shock":

        impact="energy cost spike"
        risk=base+10

    else:

        impact="unknown scenario"
        risk=base

    return {

        "scenario":s,
        "impact":impact,
        "projected_risk":round(risk,2)

    }

# -----------------------------
# BUSINESS ENGINE
# -----------------------------

def business_engine(cost,revenue):

    profit=revenue-cost

    if revenue==0:
        margin=0
    else:
        margin=(profit/revenue)*100

    if profit<0:

        risk="high"
        advice="business losing money"

    elif margin<20:

        risk="medium"
        advice="margin fragile"

    else:

        risk="low"
        advice="model sustainable"

    return {

        "profit":round(profit,2),
        "margin":round(margin,2),
        "risk":risk,
        "recommendation":advice

    }

# -----------------------------
# TRADE ENGINE
# -----------------------------

def trade_engine(q,c,p,d):

    logistics=q*d*0.7
    goods=q*c

    total=goods+logistics
    revenue=q*p

    profit=revenue-total

    if revenue==0:
        margin=0
    else:
        margin=(profit/revenue)*100

    return {

        "logistics_cost":round(logistics,2),
        "goods_cost":round(goods,2),
        "total_cost":round(total,2),
        "revenue":round(revenue,2),
        "profit":round(profit,2),
        "margin":round(margin,2)

    }

# -----------------------------
# CHAT ENGINE
# -----------------------------

def chat_engine(q):

    q=q.lower()

    if "gold" in q:
        return "Gold often performs well during inflation."

    if "economy" in q:
        return "Economic conditions depend on inflation, interest rates and liquidity."

    if "business" in q:
        return "A strong business requires stable demand and good margins."

    if "trade" in q:
        return "Trade profitability depends on margin and logistics cost."

    return "ZENTRA AI analyzing economic context."

# -----------------------------
# API
# -----------------------------

@app.get("/")
def root():

    return {"system":"ZENTRA ECONOMIC OS ACTIVE"}

@app.get("/brain")
def brain():

    return economic_brain()

@app.get("/global-risk")
def risk():

    return {"countries":global_risk()}

@app.post("/chat")
def chat(req:ChatRequest):

    return {
        "question":req.question,
        "answer":chat_engine(req.question)
    }

@app.post("/business")
def business(req:BusinessRequest):

    return business_engine(
        req.cost,
        req.revenue
    )

@app.post("/trade")
def trade(req:TradeRequest):

    return trade_engine(
        req.quantity,
        req.unit_cost,
        req.unit_price,
        req.distance
    )

@app.post("/scenario")
def scenario(req:ScenarioRequest):

    return scenario_engine(req.scenario)
