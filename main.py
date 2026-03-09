from fastapi import FastAPI
from pydantic import BaseModel
import random
import datetime

app = FastAPI(title="ZENTRA AI CORE")

# -----------------------------
# BASIC ECONOMIC DATA
# -----------------------------

def macro_environment():

    inflation = random.uniform(3,9)
    interest = random.uniform(2,8)
    liquidity = random.uniform(30,80)

    pressure = (inflation*0.4 + interest*0.3 + (100-liquidity)*0.3)

    if pressure > 60:
        state="high pressure"
    elif pressure >40:
        state="moderate pressure"
    else:
        state="stable"

    return {
        "inflation":round(inflation,2),
        "interest":round(interest,2),
        "liquidity":round(liquidity,2),
        "state":state,
        "pressure":round(pressure,2)
    }

# -----------------------------
# ECONOMIC BRAIN
# -----------------------------

def economic_brain():

    macro = macro_environment()

    if macro["pressure"]>60:
        insight="financial stress rising"
        advice="protect liquidity and reduce exposure"

    elif macro["pressure"]>40:
        insight="balanced but fragile environment"
        advice="diversify and manage risk"

    else:
        insight="economic conditions stable"
        advice="growth opportunities exist"

    return {
        "macro":macro,
        "insight":insight,
        "advice":advice
    }

# -----------------------------
# CHAT ENGINE
# -----------------------------

class ChatRequest(BaseModel):
    question:str

def chat_engine(question):

    q=question.lower()

    if "gold" in q or "altın" in q:
        return "Gold performs well during inflation periods."

    if "business" in q or "iş" in q:
        return "A good business requires stable demand and cost control."

    if "economy" in q or "ekonomi" in q:
        return "Economic conditions depend on inflation, interest rates and liquidity."

    return "ZENTRA AI is analyzing your question within economic context."

# -----------------------------
# BUSINESS SIMULATION
# -----------------------------

class BusinessRequest(BaseModel):

    cost:float
    revenue:float

def business_simulation(cost,revenue):

    profit=revenue-cost

    if profit<0:
        risk="high"
    elif profit<2000:
        risk="medium"
    else:
        risk="low"

    return {
        "profit":profit,
        "risk":risk
    }

# -----------------------------
# TRADE ENGINE
# -----------------------------

class TradeRequest(BaseModel):

    quantity:float
    unit_cost:float
    unit_price:float
    distance:float

def trade_engine(q,c,p,d):

    logistics=d*0.7*q
    goods=q*c

    total=goods+logistics

    revenue=q*p

    profit=revenue-total

    return {
        "logistics_cost":logistics,
        "total_cost":total,
        "profit":profit
    }

# -----------------------------
# ENDPOINTS
# -----------------------------

@app.get("/")
def root():

    return {"system":"ZENTRA AI CORE ACTIVE"}

@app.get("/brain")
def brain():

    return economic_brain()

@app.post("/chat")
def chat(req:ChatRequest):

    answer=chat_engine(req.question)

    return {
        "question":req.question,
        "answer":answer
    }

@app.post("/business")
def business(req:BusinessRequest):

    result=business_simulation(req.cost,req.revenue)

    return result

@app.post("/trade")
def trade(req:TradeRequest):

    result=trade_engine(
        req.quantity,
        req.unit_cost,
        req.unit_price,
        req.distance
    )

    return result
