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
import pyarrow.parquet as pq
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
    con = duckdb.connect()
    # Guardrail: cap a single query's working memory. A normal customer-filtered
    # query uses far less than this, so it's not a throttle — it only forces a
    # runaway/unfiltered query to spill to disk instead of ballooning the
    # process (which would take OLE down with it, since it's one app).
    con.execute("SET memory_limit='1GB'")
    return con


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
    """
    Lightweight readiness probe — safe to poll.

    Tells you: is the service up, are the mart files present, how many rows
    each has, and whether an ingest is currently running. Row counts come from
    the parquet FOOTER metadata (a few KB), so NO data is loaded into memory.
    """
    status = {}
    for key, path in CT_MART.items():
        if path.exists():
            try:
                status[key] = {"exists": True, "rows": pq.ParquetFile(path).metadata.num_rows}
            except Exception:
                status[key] = {"exists": True, "rows": "unknown"}
        else:
            status[key] = {"exists": False, "rows": 0}
    return {
        "status":  "ok" if status.get("pivoted", {}).get("exists") else "not_ready",
        "refresh": _get_status_snapshot()["state"],   # idle | running | success | failed
        "mart":    status,
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


@router.get("/coverage")
def ct_coverage():
    """
    Per-customer cycle-time data coverage in ONE pass over raw.parquet:
      → [ { "customer": "ASP", "assemblies": 337, "updated_on": "2026-06-02..." }, ... ]

    `assemblies` = distinct assemblies that actually have cycle-time data
    locally (contrast with the catalog total in /customers). Powers the
    Workcells league table without a per-customer /profile round trip.
    Returns [] when nothing is ingested yet (mart absent).
    """
    if not CT_MART["raw"].exists():
        return []

    con = _con()
    try:
        _load_parquet(con, "raw", "ct_raw")
        df = con.execute(
            """
            SELECT customer,
                   COUNT(DISTINCT assembly) AS assemblies,
                   MAX(updated_on)          AS updated_on
            FROM ct_raw
            GROUP BY customer
            """
        ).df()
        return _df_to_json(df)
    finally:
        con.close()


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
    # Drop alias columns that ended up entirely null after the per-page pivot —
    # same rationale as /data.
    pivoted = pivoted.dropna(axis=1, how="all")

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
        # `order` is a SQL keyword → quote it. We carry it so the FE can sort the
        # wide-table process columns by physical flow (min order per alias).
        df = con.execute(
            f"""
            SELECT alias, process, sub_workcenter, "order" AS step_order
            FROM ct_raw
            {where}
            """
        ).df()
    finally:
        con.close()

    out: dict[str, dict] = {}
    if df.empty:
        return out
    for alias, sub in df.dropna(subset=["alias"]).groupby("alias"):
        procs = sorted(sub["process"].dropna().unique().tolist())
        lines = sorted(sub["sub_workcenter"].dropna().unique().tolist())
        # Canonical sequence position for this alias = its earliest order seen.
        order = sub["step_order"].dropna()
        out[str(alias)] = {
            "processes": procs,
            "lines": lines,
            "order": int(order.min()) if not order.empty else None,
        }
    return out


@router.get("/profile")
def ct_profile(
    customer: str = Query(..., description="Workcell/customer name — must match a /customers entry"),
    pareto_limit: int = Query(20, ge=5, le=60, description="Max processes in the Pareto"),
    top_limit:    int = Query(10, ge=5, le=50, description="Max assemblies in the 'longest builds' list"),
):
    """
    Workcell profile — the analytical 'story' for one customer, computed from raw.parquet.

    A *build* is one (assembly, revision, sub_workcenter) — the unit that has a
    coherent ordered process routing and a meaningful total cycle time. We never
    average cycle time across unlike assemblies (that's noise); instead the headline
    is the **bottleneck**: which process constrains the most builds.

      → {
          "customer": "ASP",
          "summary": { assemblies, builds, lines, processes, revisions, avg_fpy,
                       updated_on, bottleneck: {alias, process, builds_bottlenecked, total_builds, pct} },
          "bottleneck_pareto": [ {alias, process, builds_bottlenecked, pct}, ... ],
          "process_pareto":    [ {alias, process, occurrences, avg_seconds, total_seconds, avg_hc}, ... ],
          "lines":             [ {sub_workcenter, builds, assemblies, avg_build_seconds, total_hc}, ... ],
          "top_assemblies":    [ {assembly, revision, sub_workcenter, total_seconds, n_processes,
                                  total_hc, avg_fpy, bottleneck_alias}, ... ]
        }
    """
    if not CT_MART["raw"].exists():
        raise HTTPException(
            status_code=503,
            detail="Cycle Time raw.parquet not found. Run /api/cycle-time/refresh first.",
        )

    con = _con()
    try:
        _load_parquet(con, "raw", "ct_raw")

        # Guard: does this customer have any rows?
        n = con.execute("SELECT COUNT(*) FROM ct_raw WHERE customer = ?", [customer]).fetchone()[0]
        if n == 0:
            raise HTTPException(
                status_code=404,
                detail=f"No cycle-time data for customer '{customer}'. "
                       f"It may not be ingested yet, or has no cycle times entered in IEDB.",
            )

        # A 'build key' groups one assembly+revision+line — the routing unit.
        BUILD = "assembly || '' || revision || '' || sub_workcenter"

        # ── Summary counts ────────────────────────────────────────────────────
        summary = con.execute(
            f"""
            SELECT
              COUNT(DISTINCT assembly)              AS assemblies,
              COUNT(DISTINCT sub_workcenter)        AS lines,
              COUNT(DISTINCT alias)                 AS processes,
              COUNT(DISTINCT revision)              AS revisions,
              COUNT(DISTINCT ({BUILD}))             AS builds,
              AVG(fpy)                              AS avg_fpy,
              MAX(updated_on)                       AS updated_on
            FROM ct_raw WHERE customer = ?
            """,
            [customer],
        ).df()
        summary_row = _df_to_json(summary)[0]
        total_builds = int(summary_row["builds"] or 0)

        # ── Bottleneck per build → the hero insight ───────────────────────────
        # For each build, the process with the largest cycle time is its bottleneck.
        # Count how often each process is the bottleneck across all builds.
        bottleneck_df = con.execute(
            f"""
            WITH ranked AS (
              SELECT alias, process,
                     ROW_NUMBER() OVER (
                       PARTITION BY {BUILD}
                       ORDER BY cycle_time_per_process DESC NULLS LAST
                     ) AS rn
              FROM ct_raw WHERE customer = ?
            )
            SELECT alias,
                   ANY_VALUE(process)  AS process,
                   COUNT(*)            AS builds_bottlenecked
            FROM ranked WHERE rn = 1
            GROUP BY alias
            ORDER BY builds_bottlenecked DESC
            """,
            [customer],
        ).df()
        bottleneck_rows = _df_to_json(bottleneck_df)
        for r in bottleneck_rows:
            r["pct"] = round(100 * (r["builds_bottlenecked"] or 0) / total_builds, 1) if total_builds else 0.0

        hero = None
        if bottleneck_rows:
            top = bottleneck_rows[0]
            hero = {
                "alias":               top["alias"],
                "process":             top["process"],
                "builds_bottlenecked": top["builds_bottlenecked"],
                "total_builds":        total_builds,
                "pct":                 top["pct"],
            }
        summary_row["bottleneck"] = hero

        # ── Process Pareto (by total time contribution) ───────────────────────
        process_pareto = _df_to_json(con.execute(
            """
            SELECT alias,
                   ANY_VALUE(process)            AS process,
                   COUNT(*)                      AS occurrences,
                   AVG(cycle_time_per_process)   AS avg_seconds,
                   SUM(cycle_time_per_process)   AS total_seconds,
                   AVG(hc)                       AS avg_hc
            FROM ct_raw WHERE customer = ?
            GROUP BY alias
            ORDER BY total_seconds DESC NULLS LAST
            LIMIT ?
            """,
            [customer, pareto_limit],
        ).df())

        # ── Lines (sub_workcenter) summary ────────────────────────────────────
        lines = _df_to_json(con.execute(
            f"""
            WITH build_tot AS (
              SELECT sub_workcenter, assembly, revision,
                     SUM(cycle_time_per_process) AS tot,
                     SUM(hc)                     AS hc
              FROM ct_raw WHERE customer = ?
              GROUP BY sub_workcenter, assembly, revision
            )
            SELECT sub_workcenter,
                   COUNT(*)                 AS builds,
                   COUNT(DISTINCT assembly) AS assemblies,
                   AVG(tot)                 AS avg_build_seconds,
                   AVG(hc)                  AS avg_build_hc
            FROM build_tot
            GROUP BY sub_workcenter
            ORDER BY builds DESC
            """,
            [customer],
        ).df())

        # ── Top assemblies by total build time (with their bottleneck) ────────
        top_assemblies = _df_to_json(con.execute(
            f"""
            WITH per_proc AS (
              SELECT assembly, revision, sub_workcenter, alias, fpy, hc, cycle_time_per_process,
                     ROW_NUMBER() OVER (
                       PARTITION BY {BUILD}
                       ORDER BY cycle_time_per_process DESC NULLS LAST
                     ) AS rn
              FROM ct_raw WHERE customer = ?
            ),
            agg AS (
              SELECT assembly, revision, sub_workcenter,
                     SUM(cycle_time_per_process) AS total_seconds,
                     COUNT(*)                    AS n_processes,
                     SUM(hc)                     AS total_hc,
                     AVG(fpy)                    AS avg_fpy,
                     MAX(CASE WHEN rn = 1 THEN alias END) AS bottleneck_alias
              FROM per_proc
              GROUP BY assembly, revision, sub_workcenter
            )
            SELECT * FROM agg
            ORDER BY total_seconds DESC NULLS LAST
            LIMIT ?
            """,
            [customer, top_limit],
        ).df())

        return {
            "customer":          customer,
            "summary":           summary_row,
            "bottleneck_pareto": bottleneck_rows[:pareto_limit],
            "process_pareto":    process_pareto,
            "lines":             lines,
            "top_assemblies":    top_assemblies,
        }
    finally:
        con.close()


_PIVOT_META_COLS = [
    "customer", "division", "family", "assembly", "revision",
    "workcenter", "workcenter_type", "sub_workcenter", "priority",
]


def _customer_process_columns(con, customer: str) -> list[str]:
    """
    The process columns that actually exist for one customer in pivoted.parquet.
    The pivot names columns by COALESCE(alias, process), so the customer's
    distinct alias-or-process values from raw == its non-null pivot columns.
    Cheap (scans raw, distinct) and lets paginated /data ship a STABLE column
    set across every page (vs per-page dropna, which would shift columns).
    """
    _load_parquet(con, "raw", "ct_raw")
    rows = con.execute(
        "SELECT DISTINCT COALESCE(alias, process) AS c FROM ct_raw "
        "WHERE customer = ? AND COALESCE(alias, process) IS NOT NULL",
        [customer],
    ).fetchall()
    return [r[0] for r in rows]


@router.get("/data")
def ct_data(
    customer:      Optional[str] = Query(None, description="Filter by customer name"),
    assembly:      Optional[str] = Query(None, description="Filter by assembly number (partial match)"),
    revision:      Optional[str] = Query(None, description="Filter by revision"),
    workcenter:    Optional[str] = Query(None, description="Filter by workcenter (e.g. SMT)"),
    sub_workcenter: Optional[str] = Query(None, description="Filter by sub-workcenter"),
    family:        Optional[str] = Query(None, description="Filter by product family"),
    page:          Optional[int] = Query(None, ge=1, description="1-based page. Omit for the full (unpaginated) array."),
    page_size:     int = Query(300, ge=1, le=2000, description="Rows per page when paginating."),
):
    """
    Returns pivoted Cycle Time data — one row per assembly/revision/sub_workcenter,
    process steps (BIRTH, SCRB, GLUEB, …) as columns. The Image 2 table layout.

    Two modes:
      • page omitted → legacy full array (used by Excel export). Trims all-null
        columns via dropna.
      • page set     → paginated envelope { page, page_size, total, pages,
        has_next, columns, rows }. First page paints almost instantly; the FE
        infinite-scrolls the rest. Columns are the customer's stable set so they
        don't shift between pages.
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

        # ── Legacy full fetch (export) ────────────────────────────────────────
        if page is None:
            df = con.execute(
                f"SELECT * FROM ct_pivoted {where} ORDER BY customer, assembly, revision"
            ).df()
            df = df.dropna(axis=1, how="all")
            return _df_to_json(df)

        # ── Paginated ─────────────────────────────────────────────────────────
        total  = con.execute(f"SELECT COUNT(*) FROM ct_pivoted {where}").fetchone()[0]
        offset = (page - 1) * page_size

        # Stable, customer-scoped column set (no per-page dropna).
        pivot_cols = list(con.execute("SELECT * FROM ct_pivoted LIMIT 0").df().columns)
        if customer:
            proc_cols = [c for c in _customer_process_columns(con, customer) if c in pivot_cols]
            sel_cols = [c for c in _PIVOT_META_COLS if c in pivot_cols] + proc_cols
            sel_sql = ", ".join('"' + c.replace('"', '""') + '"' for c in sel_cols)
        else:
            proc_cols = [c for c in pivot_cols if c not in _PIVOT_META_COLS]
            sel_sql = "*"

        df = con.execute(
            # Fully-unique sort (incl. sub_workcenter) so OFFSET paging is stable
            # — a non-unique ORDER BY can skip/duplicate rows across pages.
            f"SELECT {sel_sql} FROM ct_pivoted {where} "
            f"ORDER BY customer, assembly, revision, sub_workcenter LIMIT {page_size} OFFSET {offset}"
        ).df()

        return {
            "page":      page,
            "page_size": page_size,
            "total":     total,
            "pages":     -(-total // page_size),   # ceiling division
            "has_next":  offset + len(df) < total,
            "columns":   proc_cols,
            "rows":      _df_to_json(df),
        }
    finally:
        con.close()


@router.get("/assemblies")
def ct_assemblies(
    customer:       str = Query(..., description="Customer name — must match a /customers entry"),
    sub_workcenter: Optional[str] = Query(None, description="Optional line filter — scope builds to one line"),
    assembly:       Optional[str] = Query(None, description="Optional exact assembly — returns just that one (drawer header)"),
):
    """
    Per-assembly cycle-time aggregate for the 'Assembly Analytics' (Breakdown B)
    view — computed server-side in one pass over raw.parquet so the FE never has
    to download the full pivoted dataset just to summarise it.

      → [ { assembly, family, builds, avg_total, min_total, max_total, bottleneck }, ... ]

    A unit flows SMT → TH → BE once. Within a workcenter there can be:
      • distinct operations (e.g. BE = COAT → PACK → POT) — these are different
        steps of the build and MUST be summed; and
      • alternative lines running the SAME operation (same process-set) — these
        must NOT be summed (that multiplies one unit's time by the line count);
        we keep one representative (the max).
    So per (assembly, workcenter): group builds by their process-set signature,
    take the max within each signature (dedupe alt lines), then SUM across the
    distinct signatures. Assembly cycle time = SMT + TH + BE — one unit start to
    finish. Bottleneck = the single slowest step. The per-step waterfall in the
    drawer is fetched on demand via /data?assembly=…

    Pass `sub_workcenter` to scope to one line — only assemblies built on that
    line are returned, with their stats computed from that line's builds.
    """
    if not CT_MART["raw"].exists():
        raise HTTPException(
            status_code=503,
            detail="Cycle Time raw.parquet not found. Run /api/cycle-time/refresh first.",
        )

    # WHERE customer [AND sub_workcenter] [AND assembly] — applied to both CTEs.
    where = "WHERE customer = ?"
    scope = [customer]
    if sub_workcenter:
        where += " AND sub_workcenter = ?"
        scope.append(sub_workcenter)
    if assembly:
        where += " AND assembly = ?"
        scope.append(assembly)

    con = _con()
    try:
        _load_parquet(con, "raw", "ct_raw")
        df = con.execute(
            f"""
            WITH bp AS (
              -- per (build, workcenter): cycle time + a canonical process-set
              -- signature (sorted, so the same op-set always hashes the same).
              SELECT assembly, revision, sub_workcenter, workcenter,
                     SUM(cycle_time_per_process) AS wc_time,
                     STRING_AGG(DISTINCT COALESCE(alias, process), '|'
                                ORDER BY COALESCE(alias, process)) AS procset
              FROM ct_raw {where}
              GROUP BY assembly, revision, sub_workcenter, workcenter
            ),
            rep AS (
              -- alternative lines/revisions running the SAME operation → one rep.
              SELECT assembly, workcenter, procset, MAX(wc_time) AS rep_time
              FROM bp GROUP BY assembly, workcenter, procset
            ),
            wc AS (
              -- sum the DISTINCT operations within each workcenter.
              SELECT assembly, workcenter, SUM(rep_time) AS wc_total
              FROM rep GROUP BY assembly, workcenter
            ),
            asm AS (
              SELECT assembly,
                     SUM(CASE WHEN workcenter = 'SMT' THEN wc_total ELSE 0 END) AS smt,
                     SUM(CASE WHEN workcenter = 'TH'  THEN wc_total ELSE 0 END) AS th,
                     SUM(CASE WHEN workcenter = 'BE'  THEN wc_total ELSE 0 END) AS be
              FROM wc GROUP BY assembly
            ),
            bcount AS (
              SELECT assembly,
                     COUNT(DISTINCT revision || '|' || sub_workcenter) AS builds
              FROM bp GROUP BY assembly
            ),
            meta AS (
              SELECT assembly,
                     ANY_VALUE(family)                                       AS family,
                     arg_max(COALESCE(alias, process), cycle_time_per_process) AS bottleneck
              FROM ct_raw {where}
              GROUP BY assembly
            )
            SELECT a.assembly, m.family, b.builds,
                   (a.smt + a.th + a.be) AS total,
                   a.smt, a.th, a.be, m.bottleneck
            FROM asm a
            JOIN bcount b USING (assembly)
            JOIN meta m   USING (assembly)
            ORDER BY total DESC NULLS LAST
            """,
            scope + scope,
        ).df()
        return _df_to_json(df)
    finally:
        con.close()


@router.get("/assembly-list")
def ct_assembly_list(
    customer:       str = Query(..., description="Customer name — must match a /customers entry"),
    sub_workcenter: Optional[str] = Query(None, description="Optional line filter"),
):
    """
    Lightweight per-assembly LIST for the 'Cycle Time by Assembly' page collapsed
    rows. ONE grouped pass over raw.parquet — no cycle-time math, no string
    aggregation, no second scan (contrast /assemblies which computes SMT/TH/BE
    totals). Returns only what the collapsed row renders: identity + a stage
    footprint. The per-build process detail is fetched on demand via
    /assembly-builds.

    `builds` keeps its original meaning (distinct revision×line) for the existing
    Assemblies tab. `primary_builds` counts only priority-1 routings (distinct
    revision at priority 1 — what the new Flow tab shows by default), and
    `has_alternates` flags assemblies with any priority>1 routing (drives the
    'show alternate routes' toggle).

    `revisions` = distinct revisions for the assembly (shown in the Assemblies
    table column).

      → [ { assembly, family, builds, revisions, primary_builds, has_alternates,
            has_smt, has_th, has_be, smh }, ... ]

    `smh` = Standard Manufacturing Hour (operator content per unit) =
    Σ (IMT + Hand) × (S%/100) over the primary routing, averaged across the
    assembly's priority-1 revisions. S% is the `sampling` column.
    """
    if not CT_MART["raw"].exists():
        raise HTTPException(
            status_code=503,
            detail="Cycle Time raw.parquet not found. Run /api/cycle-time/refresh first.",
        )

    where = "WHERE customer = ?"
    scope = [customer]
    if sub_workcenter:
        where += " AND sub_workcenter = ?"
        scope.append(sub_workcenter)

    con = _con()
    try:
        _load_parquet(con, "raw", "ct_raw")
        # `smh` (Standard Manufacturing Hour) = the assembly's operator content
        # per unit: SMH = (IMT + Hand) × (S%/100) summed over a build's processes,
        # where S% is the `sampling` column. Computed on the PRIMARY routing
        # (priority = 1) per revision, then averaged across the assembly's primary
        # revisions so the collapsed row carries one representative value.
        df = con.execute(
            f"""
            WITH base AS (
                SELECT * FROM ct_raw {where}
            ),
            smh AS (
                SELECT assembly, AVG(build_smh) AS smh
                FROM (
                    SELECT assembly, revision,
                           SUM((COALESCE(imt, 0) + COALESCE(hand, 0))
                               * (COALESCE(sampling, 100) / 100.0)) AS build_smh
                    FROM base
                    WHERE priority = 1
                    GROUP BY assembly, revision
                )
                GROUP BY assembly
            )
            SELECT base.assembly,
                   ANY_VALUE(base.family)                                  AS family,
                   COUNT(DISTINCT base.revision || '|' || base.sub_workcenter) AS builds,
                   COUNT(DISTINCT base.revision)                           AS revisions,
                   COUNT(DISTINCT base.revision) FILTER (WHERE base.priority = 1) AS primary_builds,
                   BOOL_OR(base.priority > 1)                              AS has_alternates,
                   BOOL_OR(base.workcenter = 'SMT')                        AS has_smt,
                   BOOL_OR(base.workcenter = 'TH')                         AS has_th,
                   BOOL_OR(base.workcenter = 'BE')                         AS has_be,
                   ANY_VALUE(smh.smh)                                      AS smh
            FROM base
            LEFT JOIN smh USING (assembly)
            GROUP BY base.assembly
            ORDER BY base.assembly
            """,
            scope,
        ).df()
        return _df_to_json(df)
    finally:
        con.close()


@router.get("/assembly-builds")
def ct_assembly_builds(
    customer:       str = Query(..., description="Customer name — must match a /customers entry"),
    assembly:       str = Query(..., description="Exact assembly number"),
    sub_workcenter: Optional[str] = Query(None, description="Optional line filter"),
):
    """
    Per-build process detail for ONE assembly — the expanded-row tables on the
    'Cycle Time by Assembly' page. Reads raw.parquet scoped to a single assembly
    (exact match → predicate pushdown), selecting only the columns the FE needs,
    so it's far lighter than the wide /data?assembly= pivoted fetch it replaces.

    Carries `priority` (routing rank — 1 = primary) and `step_order` (the IEDB
    `order` field, the physical step sequence). A complete build = one routing =
    (revision, priority); its steps can span multiple sub_workcenters and are
    sequenced globally by `step_order`. The FE groups these long rows by
    (revision, priority) and orders the steps by `step_order`.

    Also carries the IEDB step-editor columns: `grp` (group standard), `cap`
    (capacity), `n` (sample size), `sampling` (S%, 1–100), and the time
    components `lct`, `mach`, `imt`, `hand`, `pb`, `hc` (lct is sparse). NOTE the
    FE multiplies `seconds` by `n` for the displayed cycle time (per IE convention).

      → [ { revision, priority, sub_workcenter, workcenter, step, seconds,
            step_order, grp, cap, n, sampling, lct, mach, imt, hand, pb, hc,
            fpy }, ... ]
    """
    if not CT_MART["raw"].exists():
        raise HTTPException(
            status_code=503,
            detail="Cycle Time raw.parquet not found. Run /api/cycle-time/refresh first.",
        )

    where = "WHERE customer = ? AND assembly = ?"
    scope = [customer, assembly]
    if sub_workcenter:
        where += " AND sub_workcenter = ?"
        scope.append(sub_workcenter)

    con = _con()
    try:
        _load_parquet(con, "raw", "ct_raw")
        # Dedupe by (build, step): raw stores one row PER PLAYBOOK (default + each
        # numbered playbook) with the SAME cycle time, so a naive select triples
        # the steps. Collapse to one row per step — matches the pivoted table
        # (which pivots on alias). Cycle time is identical across playbooks, so
        # MAX returns the true value.
        # `order` is a SQL keyword → must be quoted. step_order = the step's
        # physical sequence (1:1 with the step within a routing). priority is in
        # the GROUP BY so each routing (1 = primary, 2+ = alternates) stays
        # separate even when steps share a sub_workcenter.
        df = con.execute(
            f"""
            SELECT revision, priority, sub_workcenter, workcenter,
                   COALESCE(alias, process)    AS step,
                   MAX(cycle_time_per_process) AS seconds,
                   MIN("order")                AS step_order,
                   MAX(cap)                    AS cap,
                   MAX(n)                      AS n,
                   MAX(sampling)               AS sampling,
                   MAX(grp)                    AS grp,
                   MAX(lct)                    AS lct,
                   MAX(mach)                   AS mach,
                   MAX(imt)                    AS imt,
                   MAX(hand)                   AS hand,
                   MAX(pb)                     AS pb,
                   MAX(hc)                     AS hc,
                   MAX(fpy)                    AS fpy
            FROM ct_raw {where}
            GROUP BY revision, priority, sub_workcenter, workcenter, COALESCE(alias, process)
            ORDER BY revision, priority, MIN("order")
            """,
            scope,
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
