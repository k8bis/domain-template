from fastapi import FastAPI
import os

from app.core.db import wait_for_db

from app.routes.health import router as health_router
from app.routes.secure import router as secure_router
from app.routes.system import router as system_router


APP_BASE_PATH = os.getenv("APP_BASE_PATH", "/")
RODELSOFT_APP = os.getenv("RODELSOFT_APP")

# =========================================================
# DATABASE CHECK
# =========================================================

wait_for_db()

# =========================================================
# APPLICATION
# =========================================================
app = FastAPI(title=RODELSOFT_APP)

internal_app = FastAPI(title=RODELSOFT_APP + " (internal)")

internal_app.include_router(health_router)
internal_app.include_router(secure_router)
internal_app.include_router(system_router)

# montaje dinámico (igual que stocks)
if APP_BASE_PATH and APP_BASE_PATH != "/":
    app.mount(APP_BASE_PATH, internal_app)
else:
    app.mount("/", internal_app)