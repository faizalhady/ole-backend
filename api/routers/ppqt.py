"""
api/routers/ppqt.py
───────────────────
FastAPI router for the PPQT module. Placeholder — overwrite with real
endpoints when the module is built out.

Mounted at /api/ppqt in api/main.py.

Endpoints (skeleton — same shape as Cycle Time so the FE-side pattern is consistent):
  GET  /api/ppqt/health   — parquet status check
  POST /api/ppqt/refresh  — trigger pipeline (background)
  GET  /api/ppqt/data     — read mart (placeholder shape)
"""

import logging

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query

from modules.ppqt.config import PPQT_MART

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ppqt", tags=["PPQT"])


def _run_ppqt_pipeline(mode: str) -> None:
    """Background worker. Errors logged, not raised (HTTP response already sent)."""
    try:
        from modules.ppqt.pipeline.refresh import run as run_refresh

        log.info(f"PPQT pipeline started (mode={mode})")
        if not run_refresh(mode=mode):
            log.error("PPQT pipeline failed — see logs above")
            return
        log.info(f"PPQT pipeline complete (mode={mode})")
    except Exception:
        log.exception("PPQT pipeline crashed")


@router.get("/health")
def ppqt_health():
    """Check which PPQT parquet files exist."""
    return {
        "status": "placeholder",
        "mart": {key: {"exists": path.exists()} for key, path in PPQT_MART.items()},
    }


@router.post("/refresh", status_code=202)
def ppqt_refresh(
    background_tasks: BackgroundTasks,
    mode: str = Query("incremental", pattern="^(incremental|full)$"),
):
    """Trigger the PPQT pipeline in the background. Returns 202 immediately."""
    background_tasks.add_task(_run_ppqt_pipeline, mode)
    return {"status": "accepted", "message": f"PPQT pipeline started (mode={mode}). Placeholder — no real work yet."}


@router.get("/data")
def ppqt_data():
    """Placeholder read endpoint. Replace with real query logic + filters."""
    raise HTTPException(
        status_code=501,
        detail="PPQT data endpoint not implemented yet — placeholder module.",
    )
