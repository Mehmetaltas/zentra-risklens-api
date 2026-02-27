# Zentra RiskLens API v1.2
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uuid
import datetime

app = FastAPI(
    title="Zentra RiskLens API",
    version="1.2",
    description="AI-powered modular risk scoring infrastructure for modern finance platforms."
)

# =========================
# API KEY SYSTEM
# =========================
VALID_API_KEYS = {
    "zentra-demo-key",
    "zentra-partner-key",
}

# =========================
# REQUEST MODEL
# =========================
class RiskRequest(BaseModel):
    amount: float
    sector: str = "general"
    sector_risk_level: int = 3        # 1–5
    payment_delay_days: int = 0
    customer_score: int = 70          # 0–100
    exposure_ratio: float = 0.2       # 0–1

# =========================
# LANDING (HTML)
# =========================
@app.get("/", response_class=HTMLResponse)
def landing():
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Zentra RiskLens</title>
  <style>
    :root {{
      --bg1:#071028; --bg2:#0b1b3a; --card:#0f2347; --text:#eaf1ff; --muted:#a9b7d6;
      --accent:#3b82f6; --ok:#22c55e;
    }}
    *{{box-sizing:border-box}}
    body{{
      margin:0; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial;
      color:var(--text);
      background: radial-gradient(1200px 600px at 50% 0%, var(--bg2), var(--bg1));
      min-height:100vh; display:flex; align-items:flex-start; justify-content:center;
      padding:64px 18px;
    }}
    .wrap{{width:min(920px, 100%);}}
    h1{{margin:0 0 10px; font-size:44px; letter-spacing:-0.5px;}}
    p{{margin:0 0 28px; color:var(--muted); font-size:16px; line-height:1.5;}}
    .row{{display:flex; gap:14px; flex-wrap:wrap; align-items:stretch;}}
    .card{{
      background: rgba(15,35,71,0.65);
      border:1px solid rgba(255,255,255,0.07);
      border-radius:16px;
      padding:18px 18px;
      min-width:260px;
      backdrop-filter: blur(8px);
      box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    }}
    .k{{color:var(--muted); font-size:13px; margin-bottom:8px;}}
    .v{{font-size:18px; font-weight:700;}}
    .badge{{
      display:inline-flex; align-items:center; gap:8px;
      padding:10px 12px; border-radius:999px;
      background: rgba(59,130,246,0.15);
      border:1px solid rgba(59,130,246,0.25);
      color:#dbeafe; font-weight:700; font-size:14px;
    }}
    .dot{{width:10px; height:10px; border-radius:999px; background:var(--ok); box-shadow:0 0 16px rgba(34,197,94,0.6);}}
    .code{{
      margin-top:18px;
      background: rgba(0,0,0,0.28);
      border:1px solid rgba(255,255,255,0.08);
      border-radius:14px;
      padding:14px;
      overflow:auto;
      color:#e5e7eb;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New";
      font-size:13px;
      line-height:1.45;
    }}
    a{{color:#93c5fd; text-decoration:none}}
    a:hover{{text-decoration:underline}}
    .footer{{margin-top:16px; color:var(--muted); font-size:13px;}}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Zentra RiskLens</h1>
    <p>AI-Powered Modular Risk Intelligence Infrastructure</p>

    <div class="row">
      <div class="card">
        <div class="k">Status</div>
        <div class="v">LIVE</div>
      </div>
      <div class="card">
        <div class="k">Version</div>
        <div class="v">{app.version}</div>
      </div>
      <div class="card" style="flex:1">
        <div class="k">Primary Endpoint</div>
        <div class="v">POST /v1/risk</div>
      </div>
      <div class="card">
        <div class="badge"><span class="dot"></span>Production Environment Active</div>
      </div>
    </div>

    <div class="code">
      <div><b>Quick test (curl):</b></div>
<pre>curl -X POST "{'https://zentrarisk.com'}/v1/risk" \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: zentra-demo-key" \\
  -d '{{"amount":1000,"sector":"retail","sector_risk_level":2,"payment_delay_days":10,"customer_score":78,"exposure_ratio":0.25}}'</pre>
      <div class="footer">
        Health: <a href="/health">/health</a> • OpenAPI: <a href="/openapi.json">/openapi.json</a>
      </div>
    </div>
  </div>
</body>
</html>
"""

# =========================
# HEALTH CHECK (JSON)
# =========================
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "zentra-risklens",
        "version": app.version,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

# =========================
# RISK ENGINE v1.2
# =========================
@app.post("/v1/risk")
def calculate_risk(request: RiskRequest, x_api_key: str = Header(None)):
    # API KEY VALIDATION
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Basic validation clamps (safe)
    sector_level = max(1, min(5, int(request.sector_risk_level)))
    delay_days = max(0, int(request.payment_delay_days))
    customer_score = max(0, min(100, int(request.customer_score)))
    exposure_ratio = max(0.0, min(1.0, float(request.exposure_ratio)))
    amount = max(0.0, float(request.amount))

    # RISK WEIGHTS
    amount_weight = min((amount / 50000.0) * 25.0, 25.0)
    sector_weight = (sector_level / 5.0) * 20.0
    delay_weight = min((delay_days / 60.0) * 25.0, 25.0)
    behavior_weight = ((100.0 - customer_score) / 100.0) * 20.0
    exposure_weight = exposure_ratio * 10.0

    risk_score = (
        amount_weight +
        sector_weight +
        delay_weight +
        behavior_weight +
        exposure_weight
    )

    # LEVEL
    if risk_score < 30:
        level = "Low"
    elif risk_score < 60:
        level = "Medium"
    else:
        level = "High"

    return {
        "request_id": str(uuid.uuid4()),
        "model_version": app.version,
        "risk_score": round(risk_score, 2),
        "risk_level": level,
        "risk_factors": {
            "amount_weight": round(amount_weight, 2),
            "sector_weight": round(sector_weight, 2),
            "delay_weight": round(delay_weight, 2),
            "behavior_weight": round(behavior_weight, 2),
            "exposure_weight": round(exposure_weight, 2),
        },
        "confidence": 0.91,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
