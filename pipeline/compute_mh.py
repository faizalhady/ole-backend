"""
compute_mh.py
─────────────
Builds the man-hours distribution mart at per-shift grain. Each shift's paid
hours are split into named loss buckets so the 4Q Paynter chart (and any future
drill-down view) can roll the data up to day / week / month without extra math.

Output  (data/mart/)
  mh_distribution.parquet

Schema  (one row per workcell + date + shift)
  workcell                   str
  date                       date
  shift                      int
  nva_hours                  float   — from ole_computed.nva_hours
  lunch_hours                float   — va_count × 1.3
  mfg_dt_hours               float   — va_count × 0.25  (allowance)
  downtime_hours             float   — Σ(dl_affected × minutes / 60) from SQLite
  mfg_lost_hours             float   — residual clamped to ≥0 (chart-safe)
  mfg_lost_raw_hours         float   — residual without clamp; negative when
                                       the named buckets over-explain the loss
                                       (useful for data-quality audits)
  total_paid_hours           float   — denominator for any %
  effective_output_smh       float   — productive output expressed in hours

Math (percentage-driven residual; can go negative)
  named_total    = output + nva + lunch + mfg_dt + downtime
  named_pct      = named_total / total_paid_hours          (> 1 when named over-explains)
  mfg_lost_pct   = 1 − named_pct                           (negative when named over-explains)
  mfg_lost_hours = total_paid_hours × mfg_lost_pct         (signed; equivalent to paid − named)

  Equivalent simpler form: mfg_lost_hours = paid − named.
  This makes the displayed percentage `mfg_lost_hours / paid` equal mfg_lost_pct,
  so the row's % matches the residual-of-100% definition exactly.

  mfg_lost_raw_hours is kept as an alias for backward compatibility.

Buckets are stored as HOURS (not %). The chart layer computes weighted % at
display time, so 4-week averages stay mathematically correct regardless of
weekly paid-hour variation.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
import pandas as pd

from config import MART
from database import get_conn

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
log = logging.getLogger(__name__)

LUNCH_HRS_PER_VA  = 1.3
MFG_DT_HRS_PER_VA = 0.25


def _load_downtime_per_shift() -> pd.DataFrame:
    """Aggregate downtime_logs into per (workcell, date, shift) hours."""
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT workcell, date, shift,
                   SUM(dl_affected * minutes / 60.0) AS downtime_hours
            FROM downtime_logs
            GROUP BY workcell, date, shift
            """
        ).fetchall()
    if not rows:
        return pd.DataFrame(columns=["workcell", "date", "shift", "downtime_hours"])
    df = pd.DataFrame([dict(r) for r in rows])
    df["date"]  = pd.to_datetime(df["date"], errors="coerce").dt.date
    df["shift"] = df["shift"].astype(int)
    df["downtime_hours"] = df["downtime_hours"].astype(float)
    return df


def run() -> bool:
    log.info("=" * 60)
    log.info("COMPUTE MH-DISTRIBUTION  starting")
    log.info("=" * 60)

    if not MART["ole"].exists():
        log.error(f"ole_computed.parquet not found at {MART['ole']} -- run compute.py first.")
        return False

    ole = pd.read_parquet(MART["ole"])
    if ole.empty:
        log.warning("ole_computed.parquet is empty -- nothing to compute.")
        return False

    # Normalise key columns
    ole["date"]  = pd.to_datetime(ole["date"], errors="coerce").dt.date
    ole["shift"] = ole["shift"].astype(int)

    keep_cols = [
        "workcell", "date", "shift",
        "nva_hours", "va_count",
        "total_input_hours", "effective_output_smh",
    ]
    missing = [c for c in keep_cols if c not in ole.columns]
    if missing:
        log.error(f"ole_computed.parquet missing columns: {missing} -- re-run compute.py.")
        return False

    df = ole[keep_cols].copy()
    df["nva_hours"]            = df["nva_hours"].fillna(0).astype(float)
    df["va_count"]             = df["va_count"].fillna(0).astype(int)
    df["total_input_hours"]    = df["total_input_hours"].fillna(0).astype(float)
    df["effective_output_smh"] = df["effective_output_smh"].fillna(0).astype(float)

    # ── Allowance-based buckets (cheap arithmetic, no joins) ──────────────────
    df["lunch_hours"]  = (df["va_count"] * LUNCH_HRS_PER_VA).round(4)
    df["mfg_dt_hours"] = (df["va_count"] * MFG_DT_HRS_PER_VA).round(4)

    # ── Downtime (left join: ole shifts that have no downtime row get 0) ──────
    dt = _load_downtime_per_shift()
    if not dt.empty:
        df = df.merge(dt, on=["workcell", "date", "shift"], how="left")
    else:
        df["downtime_hours"] = 0.0
    df["downtime_hours"] = df["downtime_hours"].fillna(0).astype(float).round(4)

    # ── MFG Man Hour Lost (signed residual; matches the % view) ──────────────
    # named_total  = output + nva + lunch + mfg_dt + downtime
    # mfg_lost     = paid − named_total  (signed)
    # Equivalent: paid × (1 − named/paid). Negative when named over-explains paid.
    # Using paid − named keeps row %s additive: mfg_lost/paid = 1 − Σ(other%/paid).
    named_total = (
        df["effective_output_smh"]
        + df["nva_hours"]
        + df["lunch_hours"]
        + df["mfg_dt_hours"]
        + df["downtime_hours"]
    )
    df["mfg_lost_hours"]     = (df["total_input_hours"] - named_total).round(4)
    df["mfg_lost_raw_hours"] = df["mfg_lost_hours"]   # alias retained for back-compat

    # ── Rename + final shape ──────────────────────────────────────────────────
    df = df.rename(columns={"total_input_hours": "total_paid_hours"})
    out = df[[
        "workcell", "date", "shift",
        "nva_hours", "lunch_hours", "mfg_dt_hours",
        "downtime_hours", "mfg_lost_hours", "mfg_lost_raw_hours",
        "total_paid_hours", "effective_output_smh",
    ]].copy()
    out["nva_hours"] = out["nva_hours"].round(4)

    out.to_parquet(MART["mh_distribution"], index=False)
    log.info(f"mh_distribution.parquet -> {len(out)} rows written")

    # ── Sanity summary ────────────────────────────────────────────────────────
    summary = (
        out.groupby("workcell")
        .agg(
            shifts=("date", "count"),
            paid_hrs=("total_paid_hours", "sum"),
            output_hrs=("effective_output_smh", "sum"),
            nva=("nva_hours", "sum"),
            lunch=("lunch_hours", "sum"),
            mfg_dt=("mfg_dt_hours", "sum"),
            downtime=("downtime_hours", "sum"),
            mfg_lost=("mfg_lost_hours", "sum"),
        )
        .round(1)
    )
    log.info("\n" + summary.to_string())
    log.info("COMPUTE MH-DISTRIBUTION  complete")
    return True


if __name__ == "__main__":
    run()
