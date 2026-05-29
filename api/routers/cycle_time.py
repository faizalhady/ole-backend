"""
api/routers/cycle_time.py
──────────────────────────
FastAPI router for the Cycle Time module.
Mounted at /api/cycle-time in api/main.py.

Endpoints:
  GET  /api/cycle-time/health        — parquet status check
  POST /api/cycle-time/refresh       — trigger full pipeline (ingest + transform)
  GET  /api/cycle-time/customers     — list of configured customers
  GET  /api/cycle-time/data          — pivoted data (Image 2 layout), with filters
  GET  /api/cycle-time/raw           — raw row-per-process data, with filters
"""

import logging
import math
import threading
from datetime import datetime
from typing import Optional

import duckdb
import pandas as pd
from fastapi import APIRouter, BackgroundTasks, HTTPException, Query

from modules.cycle_time.config import CT_CUSTOMERS, CT_MART

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/cycle-time", tags=["Cycle Time"])


# ─── Refresh status (in-process, single source of truth) ─────────────────────
# Mutated by the BackgroundTasks worker, read by GET /refresh/status.
_status_lock = threading.Lock()
_refresh_status: dict = {
    "state":            "idle",     # idle | running | success | failed
    "mode":             None,
    "started_at":       None,
    "finished_at":      None,
    "customers_total":  0,
    "customers_done":   0,
    "current_customer": None,
    "last_error":       None,
}


def _set_status(**kwargs) -> None:
    with _status_lock:
        _refresh_status.update(kwargs)


def _get_status_snapshot() -> dict:
    with _status_lock:
        return dict(_refresh_status)


# ─── Helpers (mirrors OLE api/main.py patterns) ───────────────────────────────

def _con():
    return duckdb.connect()


def _load_parquet(con, key: str, alias: str):
    """Register a CT parquet file as a DuckDB view. Raises 503 if file missing."""
    path = CT_MART[key]
    if not path.exists():
        raise HTTPException(
            status_code=503,
            detail=f"Cycle Time mart file not found: {path.name}. Run /api/cycle-time/refresh first.",
        )
    con.execute(f"CREATE VIEW {alias} AS SELECT * FROM read_parquet('{path}')")


def _df_to_json(df: pd.DataFrame) -> list[dict]:
    """Safely convert DataFrame to JSON-serialisable list — same as OLE helper."""
    records = df.to_dict(orient="records")
    clean = []
    for row in records:
        clean_row = {}
        for k, v in row.items():
            if isinstance(v, float) and math.isnan(v):
                clean_row[k] = None
            elif not isinstance(v, (list, dict)) and pd.isna(v) if hasattr(pd, "isna") else False:
                clean_row[k] = None
            elif hasattr(v, "item"):
                clean_row[k] = v.item()
            elif hasattr(v, "isoformat"):
                clean_row[k] = v.isoformat()
            else:
                clean_row[k] = v
        clean.append(clean_row)
    return clean


def _build_where(clauses: list[str]) -> str:
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


# ─── Routes ───────────────────────────────────────────────────────────────────

@router.get("/health")
def ct_health():
    """Check which Cycle Time parquet files exist and their row counts."""
    status = {}
    for key, path in CT_MART.items():
        if path.exists():
            try:
                df = pd.read_parquet(path, columns=[pd.read_parquet(path).columns[0]])
                status[key] = {"exists": True, "rows": len(pd.read_parquet(path))}
            except Exception:
                status[key] = {"exists": True, "rows": "unknown"}
        else:
            status[key] = {"exists": False, "rows": 0}
    return {
        "status": "ok" if status.get("pivoted", {}).get("exists") else "not_ready",
        "mart":   status,
        "customers_configured": len(CT_CUSTOMERS),
    }


def _run_ct_pipeline(mode: str) -> None:
    """Background worker: runs ingest + transform. Errors are logged, not raised
    (the HTTP response has already been sent). Updates _refresh_status throughout
    so the FE can poll GET /refresh/status."""
    _set_status(
        state="running",
        mode=mode,
        started_at=datetime.utcnow().isoformat() + "Z",
        finished_at=None,
        customers_total=len(CT_CUSTOMERS),
        customers_done=0,
        current_customer=None,
        last_error=None,
    )
    try:
        from modules.cycle_time.pipeline.ingest    import run as run_ingest
        from modules.cycle_time.pipeline.transform import run as run_transform

        log.info(f"Cycle Time pipeline started (mode={mode})")

        def _progress(current_customer, done, total):
            _set_status(current_customer=current_customer,
                        customers_done=done,
                        customers_total=total)

        if not run_ingest(mode=mode, progress_cb=_progress):
            _set_status(state="failed", finished_at=datetime.utcnow().isoformat() + "Z",
                        last_error="ingest returned False — check server logs")
            log.error("Cycle Time ingest failed — see logs above")
            return
        if not run_transform():
            _set_status(state="failed", finished_at=datetime.utcnow().isoformat() + "Z",
                        last_error="transform returned False — check server logs")
            log.error("Cycle Time transform failed — see logs above")
            return
        _set_status(state="success", finished_at=datetime.utcnow().isoformat() + "Z",
                    customers_done=len(CT_CUSTOMERS), current_customer=None)
        log.info(f"Cycle Time pipeline complete (mode={mode})")
    except Exception as e:
        _set_status(state="failed", finished_at=datetime.utcnow().isoformat() + "Z",
                    last_error=str(e))
        log.exception("Cycle Time pipeline crashed")


@router.post("/refresh", status_code=202)
def ct_refresh(
    background_tasks: BackgroundTasks,
    mode: str = Query("incremental", regex="^(incremental|full)$"),
):
    """
    Trigger the Cycle Time pipeline in the background.
    Returns immediately with 202 Accepted — the pull runs after the response is sent.
    Check /api/cycle-time/health to see when the parquets are updated.

    mode=incremental (default) — only fetch records updated since last run.
    mode=full                  — re-fetch everything from the API.
    """
    if _get_status_snapshot()["state"] == "running":
        raise HTTPException(status_code=409, detail="A refresh is already running. Poll /refresh/status.")
    background_tasks.add_task(_run_ct_pipeline, mode)
    return {"status": "accepted", "message": f"Cycle Time pipeline started (mode={mode}). Poll /refresh/status."}


@router.get("/refresh/status")
def ct_refresh_status():
    """Current refresh state. Poll while state=='running' to show progress in the UI."""
    return _get_status_snapshot()


@router.get("/customers")
def ct_customers():
    """List all configured Penang customers for the Cycle Time module."""
    return CT_CUSTOMERS


@router.get("/live")
def ct_live(
    customer:        str = Query(..., description="Customer name (case-sensitive — must match /customers entry)"),
    page:            int = Query(1,   ge=1, description="IEDB page number"),
    page_size:       int = Query(500, ge=50, le=2000, description="IEDB rows per page"),
    sub_workcenter:  Optional[str] = Query(None, description="Optional line filter"),
):
    """
    Live proxy to IEDB — pivots ONE API page on-the-fly into the same row shape
    as /data, without touching the local parquet mart. Each call burns one
    IEDB API call.

      → {
          "page":        1,
          "page_size":   500,
          "total_count": 9708,
          "pages":       20,
          "has_next":    true,
          "rows":        [...pivoted rows...],
          "alias_map":   { "MA 1": { "processes": [...], "lines": [...] }, ... },
          "note":        "Assemblies spanning a page boundary may appear with partial process columns."
        }

    NOTE: pivot is page-local. An assembly whose processes span pages will
    appear in both pages, each with a subset of process columns filled.
    For complete pivoting use the DB mode (/data) after a successful ingest.
    """
    # Look up the IEDB Division for this customer (required for the API).
    cust_cfg = next((c for c in CT_CUSTOMERS if c["customer"].lower() == customer.lower()), None)
    if cust_cfg is None:
        raise HTTPException(
            status_code=404,
            detail=f"Customer '{customer}' is not configured. See /api/cycle-time/customers.",
        )

    # Defer the import so the router doesn't fail to import if requests isn't installed yet.
    try:
        from modules.cycle_time.client import fetch_page
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Live client unavailable: {e}")

    try:
        batch = fetch_page(
            customer  = cust_cfg["customer"],
            division  = cust_cfg["division"],
            page      = page,
            page_size = page_size,
        )
    except PermissionError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        log.exception("Live fetch failed")
        raise HTTPException(status_code=502, detail=f"IEDB call failed: {e}")

    if not batch:
        return {
            "page":        page,
            "page_size":   page_size,
            "total_count": 0,
            "pages":       0,
            "has_next":    False,
            "rows":        [],
            "alias_map":   {},
            "note":        "No rows for this page.",
        }

    # Normalise to snake_case (same regex as ingest.py — handles PascalCase too).
    import re
    def _snake(name: str) -> str:
        s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()

    df = pd.DataFrame(batch)
    df.columns = [_snake(c) for c in df.columns]

    # Optional sub_workcenter filter (case-sensitive — matches IEDB).
    if sub_workcenter and "sub_workcenter" in df.columns:
        df = df[df["sub_workcenter"] == sub_workcenter]

    # Pull total_count from first row (IEDB embeds it on every record).
    total_count = int(df["total_count"].iloc[0]) if "total_count" in df.columns and len(df) else 0
    pages = -(-total_count // page_size) if total_count > 0 else 0  # ceiling div

    # Pivot: alias → cycle_time_per_process, index = identity cols.
    index_cols = [c for c in [
        "customer", "division", "family", "assembly", "revision",
        "workcenter", "workcenter_type", "sub_workcenter",
    ] if c in df.columns]

    df["cycle_time_per_process"] = pd.to_numeric(df.get("cycle_time_per_process"), errors="coerce")
    if "alias" not in df.columns:
        # Fallback: if alias is missing, use process. Shouldn't happen for IEDB but safe.
        df["alias"] = df.get("process", "(no name)")
    df["alias"] = df["alias"].fillna("(no alias)")

    pivoted = (
        df.pivot_table(
            index=index_cols,
            columns="alias",
            values="cycle_time_per_process",
            aggfunc="first",
        )
        .reset_index()
    )
    pivoted.columns.name = None

    # Build alias_map from this page's rows.
    alias_map: dict[str, dict[str, list[str]]] = {}
    if "process" in df.columns:
        for alias, sub in df.dropna(subset=["alias"]).groupby("alias"):
            procs = sorted(sub["process"].dropna().unique().tolist())
            lines = sorted(sub["sub_workcenter"].dropna().unique().tolist()) \
                if "sub_workcenter" in df.columns else []
            alias_map[str(alias)] = {"processes": procs, "lines": lines}

    return {
        "page":        page,
        "page_size":   page_size,
        "total_count": total_count,
        "pages":       pages,
        "has_next":    page < pages,
        "rows":        _df_to_json(pivoted),
        "alias_map":   alias_map,
        "note":        "Per-page pivot. Assemblies spanning a page boundary may appear with partial process columns.",
    }


@router.get("/aliases")
def ct_aliases(customer: Optional[str] = Query(None, description="Scope by customer")):
    """
    For each distinct `alias` (the customer-facing process name pivoted into
    column headers), return the underlying `process` code(s) and a sample of
    the lines on which it appears.

    Used by the FE to render Process info in the column-header tooltip
    when the table is pivoted on Alias.

      → { "MA 1": { "processes": ["Assembly 1"], "lines": ["ASP HLA ENDO P1B-2", ...] }, ... }
    """
    if not CT_MART["raw"].exists():
        raise HTTPException(
            status_code=503,
            detail="Cycle Time raw.parquet not found. Run /api/cycle-time/refresh first.",
        )
    con = _con()
    try:
        _load_parquet(con, "raw", "ct_raw")
        where = f"WHERE customer = '{customer}'" if customer else ""
        df = con.execute(
            f"""
            SELECT alias, process, sub_workcenter
            FROM ct_raw
            {where}
            """
        ).df()
    finally:
        con.close()

    out: dict[str, dict[str, list[str]]] = {}
    if df.empty:
        return out
    for alias, sub in df.dropna(subset=["alias"]).groupby("alias"):
        procs = sorted(sub["process"].dropna().unique().tolist())
        lines = sorted(sub["sub_workcenter"].dropna().unique().tolist())
        out[str(alias)] = {"processes": procs, "lines": lines}
    return out


@router.get("/data")
def ct_data(
    customer:      Optional[str] = Query(None, description="Filter by customer name"),
    assembly:      Optional[str] = Query(None, description="Filter by assembly number (partial match)"),
    revision:      Optional[str] = Query(None, description="Filter by revision"),
    workcenter:    Optional[str] = Query(None, description="Filter by workcenter (e.g. SMT)"),
    sub_workcenter: Optional[str] = Query(None, description="Filter by sub-workcenter"),
    family:        Optional[str] = Query(None, description="Filter by product family"),
):
    """
    Returns pivoted Cycle Time data — one row per assembly/revision/sub_workcenter,
    process steps (BIRTH, SCRB, GLUEB, …) as columns.
    This is the Image 2 table layout.
    """
    con = _con()
    try:
        _load_parquet(con, "pivoted", "ct_pivoted")

        clauses = []
        if customer:       clauses.append(f"customer = '{customer}'")
        if assembly:       clauses.append(f"assembly ILIKE '%{assembly}%'")
        if revision:       clauses.append(f"revision = '{revision}'")
        if workcenter:     clauses.append(f"workcenter = '{workcenter}'")
        if sub_workcenter: clauses.append(f"sub_workcenter = '{sub_workcenter}'")
        if family:         clauses.append(f"family ILIKE '%{family}%'")

        where = _build_where(clauses)
        df = con.execute(
            f"SELECT * FROM ct_pivoted {where} ORDER BY customer, assembly, revision"
        ).df()
        return _df_to_json(df)
    finally:
        con.close()


@router.get("/raw")
def ct_raw(
    customer:       Optional[str] = Query(None),
    assembly:       Optional[str] = Query(None),
    revision:       Optional[str] = Query(None),
    workcenter:     Optional[str] = Query(None),
    sub_workcenter: Optional[str] = Query(None),
    process:        Optional[str] = Query(None, description="Filter by process name (e.g. BIRTH, SCRB)"),
    page:           int = Query(1, ge=1),
    page_size:      int = Query(500, ge=1, le=2000),
):
    """
    Returns raw Cycle Time data — one row per (assembly, revision, sub_workcenter, process).
    Paginated. Use /data for the pivoted (Image 2) view.
    """
    con = _con()
    try:
        _load_parquet(con, "raw", "ct_raw")

        clauses = []
        if customer:       clauses.append(f"customer = '{customer}'")
        if assembly:       clauses.append(f"assembly ILIKE '%{assembly}%'")
        if revision:       clauses.append(f"revision = '{revision}'")
        if workcenter:     clauses.append(f"workcenter = '{workcenter}'")
        if sub_workcenter: clauses.append(f"sub_workcenter = '{sub_workcenter}'")
        if process:        clauses.append(f"process = '{process}'")

        where  = _build_where(clauses)
        offset = (page - 1) * page_size

        total = con.execute(f"SELECT COUNT(*) FROM ct_raw {where}").fetchone()[0]
        df    = con.execute(
            f"SELECT * FROM ct_raw {where} ORDER BY customer, assembly, revision, process "
            f"LIMIT {page_size} OFFSET {offset}"
        ).df()

        return {
            "total":     total,
            "page":      page,
            "page_size": page_size,
            "pages":     -(-total // page_size),   # ceiling division
            "data":      _df_to_json(df),
        }
    finally:
        con.close()
