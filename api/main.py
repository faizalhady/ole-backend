import uvicorn
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
import math
from typing import Optional

import duckdb
import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import MART, WORKCELL_CONFIG, ACTIVE_WORKCELLS, INDIRECT_LABOR_CONFIG
from database import init_db, get_conn

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

# Initialise SQLite on startup
@app.on_event("startup")
def startup():
    init_db()
    log.info("SQLite operational DB ready")


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _con():
    return duckdb.connect()


def _parquet(con, key, alias=None):
    path = MART[key]
    if not path.exists():
        raise HTTPException(
            status_code=503,
            detail=f"Mart file not found: {path.name}. Run /api/refresh first.",
        )
    view_name = alias or key.replace("-", "_")
    con.execute(f"CREATE VIEW {view_name} AS SELECT * FROM read_parquet('{path}')")


def _df_to_json(df):
    records = df.to_dict(orient="records")
    clean = []
    for row in records:
        clean_row = {}
        for k, v in row.items():
            if isinstance(v, float) and math.isnan(v):
                clean_row[k] = None
            elif pd.isna(v) if not isinstance(v, (list, dict)) else False:
                clean_row[k] = None
            elif hasattr(v, "item"):
                clean_row[k] = v.item()
            elif hasattr(v, "isoformat"):
                clean_row[k] = v.isoformat()
            else:
                clean_row[k] = v
        clean.append(clean_row)
    return clean


def _where(workcell=None, date_from=None, date_to=None, date_col="date", plant=None):
    clauses = []
    if workcell:
        clauses.append(f"workcell = '{workcell}'")
    if plant:
        wcs = [wc for wc, cfg in WORKCELL_CONFIG.items() if cfg["plant"] == plant]
        if wcs:
            quoted = ", ".join(f"'{w}'" for w in wcs)
            clauses.append(f"workcell IN ({quoted})")
        else:
            clauses.append("1=0")
    if date_from:
        clauses.append(f"{date_col} >= '{date_from}'")
    if date_to:
        clauses.append(f"{date_col} <= '{date_to}'")
    return ("WHERE " + " AND ".join(clauses)) if clauses else ""


def _row_to_dict(row) -> dict:
    """Convert sqlite3.Row to plain dict."""
    return dict(row)


# ─── Shift constants (single source of truth) ─────────────────────────────────
# 1 = Normal   2 = Night   3 = Day
SHIFT_LABELS = {1: "Normal", 2: "Night", 3: "Day"}


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/api/health")
def health():
    mart_files = {key: path.exists() for key, path in MART.items()}
    return {
        "status": "ok",
        "mart_ready": all(mart_files.values()),
        "timestamp": pd.Timestamp.now().isoformat(),
        "mart_files": mart_files,
    }


@app.post("/api/refresh")
def refresh():
    try:
        from pipeline.ingest import run as ingest_run
        from pipeline.compute import run as compute_run
        from pipeline.compute_weekly import run as weekly_run

        log.info("Refresh triggered via API")
        if not ingest_run():
            raise HTTPException(status_code=500, detail="Ingest failed — check server logs.")
        if not compute_run():
            raise HTTPException(status_code=500, detail="Compute failed — check server logs.")
        if not weekly_run():
            raise HTTPException(status_code=500, detail="Weekly compute failed — check server logs.")
        return {"status": "ok", "message": "Pipeline refresh complete."}
    except HTTPException:
        raise
    except Exception as e:
        log.exception("Refresh failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/workcells")
def get_workcells():
    return [
        {
            "workcell":    wc,
            "scan_stage":  cfg["scan_stage"],
            "stage_label": cfg["label"],
            "plant":       cfg["plant"],
            "smh_column":  cfg["smh_col"],
        }
        for wc, cfg in WORKCELL_CONFIG.items()
    ]


@app.get("/api/shifts")
def get_shifts():
    """Shift reference — single source of truth for all frontend dropdowns."""
    return [{"value": k, "label": v} for k, v in SHIFT_LABELS.items()]


@app.get("/api/ole")
def get_ole(
    workcell:  Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to:   Optional[str] = Query(None),
    shift:     Optional[int] = Query(None),
):
    con = _con()
    try:
        _parquet(con, "ole")
        clauses = []
        if workcell:   clauses.append(f"workcell = '{workcell}'")
        if date_from:  clauses.append(f"date >= '{date_from}'")
        if date_to:    clauses.append(f"date <= '{date_to}'")
        if shift:      clauses.append(f"shift = {shift}")
        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        df = con.execute(f"SELECT * FROM ole {where} ORDER BY workcell, date, shift").df()
        return _df_to_json(df)
    finally:
        con.close()


@app.get("/api/ole/summary")
def get_ole_summary(
    workcell:  Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to:   Optional[str] = Query(None),
    plant:     Optional[str] = Query(None),
):
    con = _con()
    try:
        _parquet(con, "ole")
        where = _where(workcell, date_from, date_to, date_col="date", plant=plant)
        sql = f"""
        SELECT
            workcell,
            stage_label,
            scan_stage,
            COUNT(*)                                          AS total_shifts,
            ROUND(AVG(ole_pct), 2)                           AS avg_ole_pct,
            ROUND(MIN(ole_pct), 2)                           AS min_ole_pct,
            ROUND(MAX(ole_pct), 2)                           AS max_ole_pct,
            COUNT(CASE WHEN data_quality = 'OK' THEN 1 END)  AS shifts_ok,
            COUNT(CASE WHEN data_quality != 'OK' THEN 1 END) AS flagged_shifts,
            ROUND(SUM(effective_output_smh), 2)              AS total_output_smh,
            ROUND(SUM(total_input_hours), 2)                 AS total_input_hours,
            SUM(total_qty)                                   AS total_qty,
            ROUND(AVG(hc_direct), 1)                         AS avg_hc_direct,
            MIN(date)                                        AS date_from,
            MAX(date)                                        AS latest_date
        FROM ole
        {where}
        GROUP BY workcell, stage_label, scan_stage
        ORDER BY workcell
        """
        return _df_to_json(con.execute(sql).df())
    finally:
        con.close()


@app.get("/api/ole/weekly")
def get_ole_weekly(
    workcell:    Optional[str] = Query(None),
    sample_from: Optional[str] = Query(None),
    sample_to:   Optional[str] = Query(None),
    plant:       Optional[str] = Query(None),
):
    con = _con()
    try:
        _parquet(con, "ole_weekly")
        clauses = []
        if workcell:
            clauses.append(f"workcell = '{workcell}'")
        if plant:
            wcs = [wc for wc, cfg in WORKCELL_CONFIG.items() if cfg["plant"] == plant]
            if wcs:
                quoted = ", ".join(f"'{w}'" for w in wcs)
                clauses.append(f"workcell IN ({quoted})")
            else:
                clauses.append("1=0")
        if sample_from:
            clauses.append(f"week_start_date >= '{sample_from}'")
        if sample_to:
            clauses.append(f"week_start_date <= '{sample_to}'")
        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        df = con.execute(
            f"SELECT * FROM ole_weekly {where} ORDER BY workcell, iso_year, iso_week"
        ).df()
        return _df_to_json(df)
    finally:
        con.close()


@app.get("/api/ole/pareto")
def get_ole_pareto(
    date_from: Optional[str] = Query(None),
    date_to:   Optional[str] = Query(None),
    plant:     Optional[str] = Query(None),
):
    con = _con()
    try:
        _parquet(con, "ole")
        where = _where(None, date_from, date_to, date_col="date", plant=plant)
        sql = f"""
        SELECT
            workcell,
            stage_label,
            ROUND(SUM(effective_output_smh), 2)  AS total_output_smh,
            ROUND(SUM(total_input_hours), 2)      AS total_input_hours,
            ROUND(SUM(va_hours), 2)               AS total_va_hours,
            SUM(total_qty)                        AS total_qty,
            ROUND(
                CASE WHEN SUM(total_input_hours) > 0
                THEN SUM(effective_output_smh) / SUM(total_input_hours) * 100
                ELSE NULL END, 2
            )                                     AS ole_pct,
            ROUND(
                CASE WHEN SUM(va_hours) > 0
                THEN SUM(effective_output_smh) / SUM(va_hours) * 100
                ELSE NULL END, 2
            )                                     AS ole_va_pct
        FROM ole
        {where}
        GROUP BY workcell, stage_label
        ORDER BY total_input_hours DESC
        """
        df = con.execute(sql).df()
        if df.empty:
            return []
        # Cumulative % of total input hours, computed after sorting by ole_pct DESC
        total_hrs = df["total_input_hours"].sum()
        df["cum_pct"] = (df["total_input_hours"].cumsum() / total_hrs * 100).round(1)
        df["va_pct"]  = df["ole_va_pct"]  # OLE VA = output SMH / va_hours x 100
        return _df_to_json(df)
    finally:
        con.close()


@app.get("/api/ole/mh-breakdown")
def get_mh_breakdown(
    workcell:  Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to:   Optional[str] = Query(None),
    plant:     Optional[str] = Query(None),
):
    """
    Man-hours distribution breakdown for the donut chart.
    Computed on the fly from raw_paid_hours.parquet + ole_computed.parquet.

    Slices:
      output_smh     — effective output SMH (VA productive time)
      nva_hours      — SUM(tph_direct) WHERE value_type = NVA or blank
      lunch_break    — COUNT(VA rows) x 0.25  (fixed lunch/break per VA employee)
      mfg_dt         — COUNT(VA rows) x 1.3   (estimated MFG downtime per VA employee)
      unexplained    — remainder, floored at 0
    """
    con = _con()
    try:
        _parquet(con, "paid_hours")
        _parquet(con, "ole")

        # Build WHERE for paid hours
        ph_clauses = []
        if workcell:   ph_clauses.append(f"workcell = '{workcell}'")
        if date_from:  ph_clauses.append(f"date >= '{date_from}'")
        if date_to:    ph_clauses.append(f"date <= '{date_to}'")
        if plant:
            wcs = [wc for wc, cfg in WORKCELL_CONFIG.items() if cfg["plant"] == plant]
            if wcs:
                quoted = ", ".join(f"'{w}'" for w in wcs)
                ph_clauses.append(f"workcell IN ({quoted})")
            else:
                ph_clauses.append("1=0")
        ph_where = ("WHERE " + " AND ".join(ph_clauses)) if ph_clauses else ""

        # Step 1: aggregate from raw paid hours
        ph_sql = f"""
        SELECT
            SUM(tph_direct)                                          AS total_input_hours,
            SUM(CASE WHEN value_type = 'VA'  THEN tph_direct ELSE 0 END) AS va_hours,
            SUM(CASE WHEN value_type = 'NVA' OR value_type = ''
                     THEN tph_direct ELSE 0 END)                     AS nva_hours,
            COUNT(CASE WHEN value_type = 'VA' THEN 1 END)            AS va_row_count
        FROM paid_hours
        {ph_where}
        """
        ph = con.execute(ph_sql).df().iloc[0]

        total_input_hours = float(ph["total_input_hours"] or 0)
        nva_hours         = float(ph["nva_hours"]         or 0)
        va_row_count      = float(ph["va_row_count"]      or 0)

        # Step 2: get output SMH from ole_computed
        ole_where = _where(workcell, date_from, date_to, date_col="date", plant=plant)
        ole_sql = f"""
        SELECT ROUND(SUM(effective_output_smh), 4) AS output_smh
        FROM ole
        {ole_where}
        """
        output_smh = float(con.execute(ole_sql).df().iloc[0]["output_smh"] or 0)

        # Step 3: formula-based components
        lunch_break = round(va_row_count * 0.25, 4)
        mfg_dt      = round(va_row_count * 1.3,  4)

        # Step 4: non-identified = loss pool minus identified categories. No floor — negative surfaces.
        loss_pool       = total_input_hours - output_smh
        identified      = nva_hours + lunch_break + mfg_dt
        non_identified  = round(loss_pool - identified, 4)

        return {
            "total_input_hours": round(total_input_hours, 4),
            "loss_pool":         round(loss_pool, 4),
            "slices": [
                { "name": "Output SMH",             "value": round(output_smh, 4),  "color": "#22c55e" },
                { "name": "NVA Input",              "value": round(nva_hours, 4),   "color": "#ef4444" },
                { "name": "Lunch / Break",          "value": round(lunch_break, 4), "color": "#94a3b8" },
                { "name": "MFG DT",                 "value": round(mfg_dt, 4),      "color": "#f59e0b" },
                { "name": "Unexplained Lost Hours", "value": non_identified,        "color": "#6366f1" },
            ]
        }
    finally:
        con.close()


@app.get("/api/ole/predict")
def get_ole_predict(
    workcell:         str = Query(...),
    projection_weeks: int = Query(3, ge=1, le=12),
):
    try:
        from statsmodels.tsa.arima.model import ARIMA
        from statsmodels.tsa.holtwinters import ExponentialSmoothing
        import warnings
        warnings.filterwarnings("ignore")
    except ImportError:
        raise HTTPException(status_code=501, detail="statsmodels not installed.")

    con = _con()
    try:
        _parquet(con, "ole_weekly")
        df = con.execute(
            f"SELECT * FROM ole_weekly WHERE workcell = '{workcell}' ORDER BY iso_year, iso_week"
        ).df()
    finally:
        con.close()

    if df.empty:
        raise HTTPException(status_code=404, detail=f"No weekly data for workcell '{workcell}'")

    df = df.dropna(subset=["ole_pct"]).reset_index(drop=True)
    if len(df) < 4:
        raise HTTPException(status_code=422, detail=f"Not enough data ({len(df)} weeks, need >= 4)")

    series = df["ole_pct"].values.astype(float)
    n = len(series)
    seasonal_periods = 4 if n >= 8 else None

    arima_fitted = [None] * n
    hw_fitted    = [None] * n
    for i in range(3, n):
        try:
            fit = ARIMA(series[:i], order=(1, 1, 1)).fit()
            arima_fitted[i] = round(float(fit.forecast(steps=1)[0]), 2)
        except Exception:
            pass
        try:
            kwargs = dict(trend="add", initialization_method="estimated")
            if seasonal_periods and i >= seasonal_periods * 2:
                kwargs.update(seasonal="add", seasonal_periods=seasonal_periods)
            fit = ExponentialSmoothing(series[:i], **kwargs).fit(optimized=True)
            hw_fitted[i] = round(float(fit.forecast(1)[0]), 2)
        except Exception:
            pass

    rows = [
        {
            "workcell":   workcell,
            "week_label": row["week_label"],
            "iso_year":   int(row["iso_year"]),
            "iso_week":   int(row["iso_week"]),
            "actual":     round(float(row["ole_pct"]), 2),
            "arima":      arima_fitted[i],
            "hw":         hw_fitted[i],
            "projected":  False,
        }
        for i, row in df.iterrows()
    ]

    last_year, last_week = int(df["iso_year"].iloc[-1]), int(df["iso_week"].iloc[-1])

    try:
        arima_proj = [round(float(v), 2) for v in ARIMA(series, order=(1, 1, 1)).fit().forecast(steps=projection_weeks)]
    except Exception:
        arima_proj = [None] * projection_weeks

    try:
        kwargs = dict(trend="add", initialization_method="estimated")
        if seasonal_periods and n >= seasonal_periods * 2:
            kwargs.update(seasonal="add", seasonal_periods=seasonal_periods)
        hw_proj = [round(float(v), 2) for v in ExponentialSmoothing(series, **kwargs).fit(optimized=True).forecast(projection_weeks)]
    except Exception:
        hw_proj = [None] * projection_weeks

    py, pw = last_year, last_week
    for p in range(projection_weeks):
        pw += 1
        if pw > 52:
            pw = 1
            py += 1
        rows.append({
            "workcell":   workcell,
            "week_label": f"{py}-W{str(pw).zfill(2)}",
            "iso_year":   py,
            "iso_week":   pw,
            "actual":     None,
            "arima":      arima_proj[p] if p < len(arima_proj) else None,
            "hw":         hw_proj[p]    if p < len(hw_proj)    else None,
            "projected":  True,
        })

    return rows


@app.get("/api/production")
def get_production(
    workcell:  Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to:   Optional[str] = Query(None),
):
    con = _con()
    try:
        _parquet(con, "production")
        where = _where(workcell, date_from, date_to, date_col="date")
        return _df_to_json(con.execute(f"SELECT * FROM production {where} ORDER BY workcell, date, shift").df())
    finally:
        con.close()


@app.get("/api/paid-hours")
def get_paid_hours(
    workcell:  Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to:   Optional[str] = Query(None),
):
    con = _con()
    try:
        _parquet(con, "paid_hours")
        where = _where(workcell, date_from, date_to, date_col="date")
        return _df_to_json(con.execute(f"SELECT * FROM paid_hours {where} ORDER BY workcell, date, shift").df())
    finally:
        con.close()


@app.get("/api/smh")
def get_smh(
    workcell: Optional[str] = Query(None),
    assembly: Optional[str] = Query(None),
):
    con = _con()
    try:
        _parquet(con, "smh")
        clauses = []
        if workcell:
            clauses.append(f"workcell = '{workcell}'")
        if assembly:
            clauses.append(f"assembly = '{assembly}'")
        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        return _df_to_json(con.execute(f"SELECT * FROM smh {where} ORDER BY workcell, assembly").df())
    finally:
        con.close()


@app.get("/api/smh-status")
def get_smh_status(
    workcell: Optional[str] = Query(None),
    status:   Optional[str] = Query(None),
):
    con = _con()
    try:
        _parquet(con, "smh_status")
        clauses = []
        if workcell:
            clauses.append(f"workcell = '{workcell}'")
        if status:
            clauses.append(f"smh_status = '{status}'")
        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        return _df_to_json(con.execute(
            f"SELECT * FROM smh_status {where} ORDER BY workcell, smh_status, total_qty_produced DESC"
        ).df())
    finally:
        con.close()


# ═══════════════════════════════════════════════════════════════════════════════
# INDIRECT LABOR — Warehouses, Support pools (non-workcell entities)
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/api/indirect-labor")
def get_indirect_labor(
    entity:    Optional[str] = Query(None),
    plant:     Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to:   Optional[str] = Query(None),
    shift:     Optional[int] = Query(None),
):
    """
    Returns aggregated paid hours for non-workcell entities (warehouses,
    support pools). One row per (entity, date, shift).
    """
    con = _con()
    try:
        _parquet(con, "indirect_labor")
        clauses = []
        if entity:    clauses.append(f"entity = '{entity}'")
        if plant:     clauses.append(f"plant = '{plant}'")
        if date_from: clauses.append(f"date >= '{date_from}'")
        if date_to:   clauses.append(f"date <= '{date_to}'")
        if shift:     clauses.append(f"shift = {shift}")
        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        return _df_to_json(con.execute(
            f"SELECT * FROM indirect_labor {where} ORDER BY entity, date, shift"
        ).df())
    finally:
        con.close()


@app.get("/api/indirect-labor/entities")
def get_indirect_labor_entities():
    """Return the configured indirect labor entities and their metadata."""
    return [
        {"entity": k, **v}
        for k, v in INDIRECT_LABOR_CONFIG.items()
    ]


# ═══════════════════════════════════════════════════════════════════════════════
# DOWNTIME LOGS — SQLite CRUD
# ═══════════════════════════════════════════════════════════════════════════════

class DowntimeCreate(BaseModel):
    date:        str
    shift:       int           # 1=Day  2=Night  3=Overtime
    workcell:    str
    bay:         str | None = None
    dept:        str
    code:        str
    dl_affected: int = 0
    minutes:     int
    commentary:  str | None = None


@app.get("/api/downtime")
def list_downtime(
    workcell:  Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to:   Optional[str] = Query(None),
    shift:     Optional[int] = Query(None),
):
    clauses, params = [], []
    if workcell:   clauses.append("workcell = ?");  params.append(workcell)
    if date_from:  clauses.append("date >= ?");     params.append(date_from)
    if date_to:    clauses.append("date <= ?");     params.append(date_to)
    if shift:      clauses.append("shift = ?");     params.append(shift)
    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    with get_conn() as conn:
        rows = conn.execute(
            f"SELECT * FROM downtime_logs {where} ORDER BY date DESC, shift",
            params
        ).fetchall()
    return [_row_to_dict(r) for r in rows]


@app.post("/api/downtime", status_code=201)
def create_downtime(body: DowntimeCreate):
    if body.workcell not in WORKCELL_CONFIG:
        raise HTTPException(status_code=400, detail=f"Unknown workcell: {body.workcell}")
    if body.shift not in (1, 2, 3):
        raise HTTPException(status_code=400, detail="Shift must be 1 (Normal), 2 (Night), or 3 (Day)")
    with get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO downtime_logs
               (date, shift, workcell, bay, dept, code, dl_affected, minutes, commentary)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (body.date, body.shift, body.workcell, body.bay,
             body.dept, body.code, body.dl_affected, body.minutes, body.commentary)
        )
        row = conn.execute("SELECT * FROM downtime_logs WHERE id = ?", (cur.lastrowid,)).fetchone()
    return _row_to_dict(row)


@app.delete("/api/downtime/{log_id}", status_code=204)
def delete_downtime(log_id: int):
    with get_conn() as conn:
        deleted = conn.execute("DELETE FROM downtime_logs WHERE id = ?", (log_id,)).rowcount
    if not deleted:
        raise HTTPException(status_code=404, detail="Log not found")


# ═══════════════════════════════════════════════════════════════════════════════
# TRANSFER LOGS — SQLite CRUD
# ═══════════════════════════════════════════════════════════════════════════════

class TransferCreate(BaseModel):
    date:    str
    shift:   int           # 1=Day  2=Night  3=Overtime
    from_wc: str
    to_wc:   str
    va_hc:   int  = 0
    va_hrs:  float = 0
    nva_hc:  int  = 0
    nva_hrs: float = 0


@app.get("/api/transfers")
def list_transfers(
    workcell:  Optional[str] = Query(None),   # matches from_wc OR to_wc
    date_from: Optional[str] = Query(None),
    date_to:   Optional[str] = Query(None),
    shift:     Optional[int] = Query(None),
):
    clauses, params = [], []
    if workcell:
        clauses.append("(from_wc = ? OR to_wc = ?)")
        params.extend([workcell, workcell])
    if date_from:  clauses.append("date >= ?");  params.append(date_from)
    if date_to:    clauses.append("date <= ?");  params.append(date_to)
    if shift:      clauses.append("shift = ?");  params.append(shift)
    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    with get_conn() as conn:
        rows = conn.execute(
            f"SELECT * FROM transfer_logs {where} ORDER BY date DESC, shift",
            params
        ).fetchall()
    return [_row_to_dict(r) for r in rows]


@app.post("/api/transfers", status_code=201)
def create_transfer(body: TransferCreate):
    if body.from_wc not in WORKCELL_CONFIG:
        raise HTTPException(status_code=400, detail=f"Unknown workcell (from): {body.from_wc}")
    if body.to_wc not in WORKCELL_CONFIG:
        raise HTTPException(status_code=400, detail=f"Unknown workcell (to): {body.to_wc}")
    if body.from_wc == body.to_wc:
        raise HTTPException(status_code=400, detail="from_wc and to_wc cannot be the same")
    if body.shift not in (1, 2, 3):
        raise HTTPException(status_code=400, detail="Shift must be 1 (Normal), 2 (Night), or 3 (Day)")
    with get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO transfer_logs
               (date, shift, from_wc, to_wc, va_hc, va_hrs, nva_hc, nva_hrs)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (body.date, body.shift, body.from_wc, body.to_wc,
             body.va_hc, body.va_hrs, body.nva_hc, body.nva_hrs)
        )
        row = conn.execute("SELECT * FROM transfer_logs WHERE id = ?", (cur.lastrowid,)).fetchone()
    return _row_to_dict(row)


@app.delete("/api/transfers/{log_id}", status_code=204)
def delete_transfer(log_id: int):
    with get_conn() as conn:
        deleted = conn.execute("DELETE FROM transfer_logs WHERE id = ?", (log_id,)).rowcount
    if not deleted:
        raise HTTPException(status_code=404, detail="Transfer not found")


if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
