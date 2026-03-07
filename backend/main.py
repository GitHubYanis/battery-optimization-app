from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse

import datetime
from datetime import datetime, timezone
from pydantic import BaseModel
import time
import logging
from collections import defaultdict
import os
from dotenv import load_dotenv

from battery import build_charts, build_optimize_result

load_dotenv()

API_KEY = os.getenv("API_KEY")
RATE_LIMIT = int(os.getenv("RATE_LIMIT", 100))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://battery-api.proudcliff-6f07144c.canadacentral.azurecontainerapps.io"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

rate_limit_store: dict[str, list[float]] = defaultdict(list)

@app.middleware("http")
async def auth_and_rate_limit(request: Request, call_next):
    protected_paths = ["/optimize", "/visualize"]
    if request.url.path not in protected_paths or request.method == "OPTIONS":
        return await call_next(request)
    
    api_key = request.headers.get("x-api-key")
    if api_key != API_KEY:
        return JSONResponse(status_code=401, content={"detail": "Invalid or missing API key"})

    now = time.time()
    timestamps = rate_limit_store[api_key]
    rate_limit_store[api_key] = [t for t in timestamps if now - t < 3600]  # garde seulement la dernière heure
    
    if len(rate_limit_store[api_key]) >= RATE_LIMIT:
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
    
    rate_limit_store[api_key].append(now)

    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)
    logger.info(f"{request.method} {request.url.path} - key: {api_key[:8]}... - {duration}ms - {response.status_code}")

    return response

class BatteryInfo(BaseModel):
    capacity_kwh: float
    max_charge_kw: float
    max_discharge_kw: float
    efficiency: float # entre 0 et 1 representant la charge/décharge
    initial_soc_kwh: float # le niveau de charge au départ

class BatteryRequest(BaseModel):
    load_kwh: list[float] # je suppose une consommation horaire formatée: 0h, 1h, ..., 23h et que les autres listes suivent le même format
    price_per_kwh: list[float] 
    battery: BatteryInfo

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post("/optimize")
def optimize_battery(request: BatteryRequest):
    return build_optimize_result(request.load_kwh, request.price_per_kwh, request.battery)


@app.post("/visualize")
def visualize_battery(request: BatteryRequest):
    load = request.load_kwh
    prices = request.price_per_kwh
    result = build_optimize_result(load, prices, request.battery)

    summary = {
        "total_cost_before": result["total_cost_before"],
        "total_cost_after": result["total_cost_after"],
        "savings": result["savings"],
        "peak_before_kw": max(load),
        "peak_after_kw": max(
            load[h] - result["discharge_kw"][h] + result["charge_kw"][h]
            for h in range(24)
        )
    }

    return {
        "summary": summary, 
        "charts": build_charts(load, prices, result)
    }

if os.path.exists("static"):
    from fastapi.staticfiles import StaticFiles
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
