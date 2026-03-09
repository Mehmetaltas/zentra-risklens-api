from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI(title="ZENTRA Economic OS")

# -------------------------
# MODELS
# -------------------------

class ChatRequest(BaseModel):
    question:str

class SectorRequest(BaseModel):
    sector:str
    demand:float
    cost_pressure:float
    finance_pressure:float

class SMERequest(BaseModel):
    revenue:float
    cost:float
    debt:float
    delay:int

class SupplyRequest(BaseModel):
    lead_time_days:int
    supplier_risk:float
    logistics_delay_risk:float
    inventory_buffer_days:int

class TradeRequest(BaseModel):
    origin:str
    destination:str
    product:str
    transport_cost:float
    product_price:float

# -------------------------
# ROOT
# -------------------------

@app.get("/")
def root():
    return {"system":"ZENTRA CORE ACTIVE"}

# -------------------------
# ECONOMIC BRAIN
# -------------------------

@app.get("/brain")
def brain():

    inflation=random.randint(3,9)
    interest=random.randint(4,10)

    risk=(inflation+interest)*5

    if risk>70:
        state="high pressure"
    elif risk>40:
        state="moderate pressure"
    else:
        state="stable"

    return{

        "global_risk_index":risk,
        "economic_state":state,
        "market_trend":"neutral",
        "insight":"economic pressure driven by inflation and interest",
        "advice":"maintain liquidity and monitor cost structure"

    }

# -------------------------
# GLOBAL RISK
# -------------------------

@app.get("/global-risk")
def global_risk():

    countries=[

        {"name":"United States","risk":42},
        {"name":"Germany","risk":36},
        {"name":"China","risk":48},
        {"name":"India","risk":52},
        {"name":"Turkey","risk":69},
        {"name":"Brazil","risk":55}

    ]

    return {"countries":countries}

# -------------------------
# CHAT
# -------------------------

@app.post("/chat")
def chat(req:ChatRequest):

    q=req.question.lower()

    if "inflation" in q:
        return{"answer":"Inflation reduces purchasing power and increases cost pressure."}

    if "gold" in q:
        return{"answer":"Gold often benefits during inflationary periods."}

    if "business" in q:
        return{"answer":"A healthy business requires strong cashflow and margin stability."}

    return{"answer":"ZENTRA is analyzing the economic context."}

# -------------------------
# SECTOR INTELLIGENCE
# -------------------------

@app.post("/sector-intelligence")
def sector(req:SectorRequest):

    risk=(req.cost_pressure+req.finance_pressure+(100-req.demand))/3

    if risk>70:
        band="high"
    elif risk>40:
        band="medium"
    else:
        band="low"

    return{

        "sector":req.sector,
        "sector_risk_score":risk,
        "band":band,
        "recommendation":"monitor demand and cost dynamics"

    }

# -------------------------
# SME INTELLIGENCE
# -------------------------

@app.post("/sme-intelligence")
def sme(req:SMERequest):

    profit=req.revenue-req.cost-req.debt

    risk=50

    if profit<0:
        risk+=30

    risk+=req.delay*0.5

    return{

        "profit":profit,
        "risk_score":risk

    }

# -------------------------
# SUPPLY CHAIN
# -------------------------

@app.post("/supply-chain")
def supply(req:SupplyRequest):

    risk=(req.lead_time_days*0.4+
          req.supplier_risk*0.3+
          req.logistics_delay_risk*0.2-
          req.inventory_buffer_days*0.2)

    return{

        "risk_score":risk,
        "recommendation":"increase inventory buffer or diversify suppliers"

    }

# -------------------------
# TRADE INTELLIGENCE
# -------------------------

@app.post("/trade-intelligence")
def trade(req:TradeRequest):

    margin=req.product_price-req.transport_cost

    if margin>50:
        viability="high"
    elif margin>20:
        viability="medium"
    else:
        viability="low"

    return{

        "route":f"{req.origin} → {req.destination}",
        "product":req.product,
        "margin":margin,
        "trade_viability":viability

    }

# -------------------------
# NETWORK INTELLIGENCE
# -------------------------

@app.get("/network")
def network():

    return{

        "supplier_nodes":120,
        "trade_nodes":85,
        "logistics_nodes":42,
        "market_nodes":64,
        "network_stress":48

    }

# -------------------------
# KNOWLEDGE ENGINE
# -------------------------

@app.get("/knowledge")
def knowledge(topic:str):

    if topic=="inflation":
        return{"definition":"Inflation is the rate at which prices increase."}

    if topic=="cds":
        return{"definition":"CDS measures sovereign credit risk."}

    return{"definition":"economic knowledge topic"}
