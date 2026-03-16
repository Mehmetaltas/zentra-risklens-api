from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api_market import router as market_router
from backend.api_signals import router as signals_router
from backend.api_risk import router as risk_router
from backend.api_terminal import router as terminal_router

app = FastAPI(
    title="ZENTRA V1 API",
    version="1.0.0",
    description="ZENTRA Economic Terminal + RiskLens backend"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market_router)
app.include_router(signals_router)
app.include_router(risk_router)
app.include_router(terminal_router)


@app.get("/")
def root():
    return {
        "system": "ZENTRA",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "zentra-v1-api"
    }
