# -----------------------------
# SCENARIO ENGINE
# -----------------------------

from pydantic import BaseModel

class ScenarioRequest(BaseModel):
    scenario: str


def scenario_engine(scenario, macro, market, behavior):

    inflation = macro["inflation"]
    btc = market["btc"]
    behavior_score = behavior["behavior_score"]

    if scenario == "interest_rate_shock":

        macro_risk = min(inflation / 8 + 0.3, 1)
        system_stress = macro_risk * 100

        result = {
            "scenario": "interest_rate_shock",
            "description": "central bank rate increase",
            "impact": "credit contraction and investment slowdown",
            "projected_system_stress": round(system_stress,2),
            "risk_level": "high"
        }

    elif scenario == "currency_shock":

        macro_risk = min(inflation / 7 + 0.4, 1)
        system_stress = macro_risk * 100

        result = {
            "scenario": "currency_shock",
            "description": "sharp currency depreciation",
            "impact": "import cost increase and inflation pressure",
            "projected_system_stress": round(system_stress,2),
            "risk_level": "high"
        }

    elif scenario == "oil_price_shock":

        macro_risk = min(inflation / 9 + 0.25, 1)
        system_stress = macro_risk * 100

        result = {
            "scenario": "oil_price_shock",
            "description": "energy price surge",
            "impact": "production cost increase and sector stress",
            "projected_system_stress": round(system_stress,2),
            "risk_level": "medium"
        }

    elif scenario == "demand_drop":

        business_pressure = behavior_score + 0.3
        system_stress = business_pressure * 100

        result = {
            "scenario": "demand_drop",
            "description": "consumer demand decline",
            "impact": "sales pressure and liquidity stress",
            "projected_system_stress": round(system_stress,2),
            "risk_level": "medium"
        }

    elif scenario == "credit_crunch":

        credit_pressure = behavior_score + 0.4
        system_stress = credit_pressure * 100

        result = {
            "scenario": "credit_crunch",
            "description": "credit availability tightening",
            "impact": "financing difficulty for businesses",
            "projected_system_stress": round(system_stress,2),
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
# SECTOR ENGINE
# -----------------------------

class SectorRequest(BaseModel):
    sector: str
    sales_trend: float = 0.5
    cost_pressure: float = 0.5
    demand_index: float = 0.5


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
        band = "critical"
    elif risk_score >= 60:
        band = "high"
    elif risk_score >= 40:
        band = "medium"
    else:
        band = "low"

    return round(risk_score,2), band


@app.post("/sector-risk")
def sector_risk(req: SectorRequest):

    macro = get_macro_data()
    indicators = indicator_engine(macro)
    economic = economic_engine(indicators)

    macro_risk = economic["macro_risk"]

    score, band = sector_risk_model(
        req.sector,
        req.sales_trend,
        req.cost_pressure,
        req.demand_index,
        macro_risk
    )

    return {
        "sector": req.sector,
        "sector_risk_score": score,
        "risk_band": band,
        "macro_environment": economic["economic_state"]
    }
