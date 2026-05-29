"""
api/main.py
───────────
FastAPI app entry point. Thin — only wires together middleware, startup
hooks, and module routers. Endpoint logic lives in api/routers/*.

To add a new module:
  1. Build its router in api/routers/<module>.py
  2. Import + include_router below
"""

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import init_db
from api.routers.ole         import router as ole_router
from api.routers.downtime    import router as downtime_router
from api.routers.transfers   import router as transfers_router
from api.routers.cycle_time  import router as cycle_time_router
from api.routers.ppqt        import router as ppqt_router
from api.routers.lbr         import router as lbr_router
from api.routers.ipk         import router as ipk_router


logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
log = logging.getLogger(__name__)

app = FastAPI(title="OLE Analyzer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Module routers ───────────────────────────────────────────────────────────
app.include_router(ole_router)
app.include_router(downtime_router)
app.include_router(transfers_router)
app.include_router(cycle_time_router)
app.include_router(ppqt_router)
app.include_router(lbr_router)
app.include_router(ipk_router)


@app.on_event("startup")
def startup():
    init_db()
    log.info("SQLite operational DB ready")


if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
