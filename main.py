from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI(title="ZENTRA CORE API")

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

# -----------------------------
# ECONOMIC DATA
# -----------------------------

def macro_data():

    inflation = round(random.uniform(3,9),2)
    interest = round(random.uniform(2,8),2)
    liquidity = round(random.uniform(30,85),2)
    volatility = round(random.uniform(20,80),2)

    return {
        "inflation":inflation,
        "interest":interest,
        "liquidity":liquidity,
        "volatility":volatility
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
        data["volatility"] * 0.20
    ) / 2

    risk = round(min(max(risk,0),100),2)

    if risk > 70:
        state="high pressure"
        advice="reduce risk exposure and protect liquidity"

    elif risk > 45:
        state="moderate pressure"
        advice="diversify investments and control costs"

    else:
        state="stable"
        advice="growth opportunities available"

    return {
        "global_risk_index":risk,
        "economic_state":state,
        "market_trend":"neutral",
        "insight":"macro financial pressure analysis",
        "advice":advice
    }

# -----------------------------
# GLOBAL RISK
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
# CHAT ENGINE
# -----------------------------

def chat_engine(q):

    q=q.lower()

    if "gold" in q or "altın" in q:
        return "Gold is often used as a hedge against inflation."

    if "economy" in q or "ekonomi" in q:
        return "Economic conditions depend on inflation, interest rates and liquidity."

    if "business" in q or "iş" in q:
        return "A sustainable business requires stable demand and strong cashflow."

    return "ZENTRA AI is analyzing your economic question."

# -----------------------------
# BUSINESS ENGINE
# -----------------------------

def business_engine(cost,revenue):

    profit = revenue-cost

    if revenue==0:
        margin=0
    else:
        margin=round((profit/revenue)*100,2)

    if profit<0:
        risk="high"
        rec="business losing money"

    elif margin<20:
        risk="medium"
        rec="profit exists but margin fragile"

    else:
        risk="low"
        rec="business model sustainable"

    return {
        "profit":round(profit,2),
        "margin":margin,
        "risk":risk,
        "recommendation":rec
    }

# -----------------------------
# TRADE ENGINE
# -----------------------------

def trade_engine(q,c,p,d):

    logistics = q*d*0.7
    goods = q*c

    total = logistics+goods
    revenue = q*p

    profit = revenue-total

    if revenue==0:
        margin=0
    else:
        margin=round((profit/revenue)*100,2)

    return {
        "logistics_cost":round(logistics,2),
        "goods_cost":round(goods,2),
        "total_cost":round(total,2),
        "revenue":round(revenue,2),
        "profit":round(profit,2),
        "margin":margin,
        "risk":"medium"
    }

# -----------------------------
# API
# -----------------------------

@app.get("/")
def root():
    return {"system":"ZENTRA CORE ACTIVE"}

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
