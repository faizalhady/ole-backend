"""
compute_weekly.py
─────────────────
Aggregates ole_computed.parquet (shift-level) into a weekly summary per
workcell, keyed by ISO year + ISO week number.

This mart table is the primary input for the projection engine — all
forecasting formulas (SMA, WMA, EMA, regression, Holt-Winters, etc.)
operate on weekly OLE values, not individual shifts.

Output  (data/mart/)
  ole_weekly.parquet

Schema
  workcell          str   — canonical workcell name
  iso_year          int   — ISO calendar year (e.g. 2025)
  iso_week          int   — ISO week number 1–53
  week_label        str   — human-readable label e.g. "2025-W03"
  week_start_date   date  — Monday of that ISO week
  week_end_date     date  — Sunday of that ISO week
  stage_label       str   — e.g. BoxBuild / SMT / Backend
  scan_stage        str   — raw scan stage value

  -- Output side (summed across all shifts in the week)
  total_qty               int
  total_output_smh        float
  shift_count             int   — number of shifts worked

  -- Input side (summed across all shifts in the week)
  total_input_hours       float
  avg_hc_direct           float — average headcount across shifts
  total_va_hours          float — sum of VA hours across shifts
  total_nva_hours         float — sum of NVA + blank hours across shifts

  -- OLE (computed at weekly level, not average of shift OLEs)
  ole_pct                 float — weekly OLE = (sum output SMH / sum input hrs) x 100
  ole_pct_avg_shifts      float — simple average of per-shift OLE% (for comparison)

  -- Data quality
  shifts_ok               int   — shifts with data_quality = OK
  shifts_flagged          int   — shifts with data_quality != OK
  smh_coverage_pct        float — weighted average SMH coverage across shifts
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
import duckdb
import pandas as pd

from config import MART

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
log = logging.getLogger(__name__)


def _filter_full_coverage_weeks(df: pd.DataFrame) -> pd.DataFrame:
    """
    Keep only ISO weeks where BOTH raw_production AND raw_paid_hours provide
    data for the entire Mon-Sun span.

    Why: production data and paid-hours data don't always cover the same date
    range (one source may go back further than the other due to file rotation
    / retention). A partial-coverage week would show misleading aggregates,
    e.g. WW11 with only Sunday's production data while paid hours cover the
    whole week.

    Logic:
      effective_start = max(min(production date), min(paid_hours date))
      effective_end   = min(max(production date), max(paid_hours date))
      first complete week starts at the first Monday >= effective_start
      last  complete week ends   at the last  Sunday <= effective_end
    """
    if not MART["production"].exists() or not MART["paid_hours"].exists():
        log.warning("Coverage filter: raw mart missing, skipping.")
        return df

    prod_dates  = pd.to_datetime(pd.read_parquet(MART["production"])["date"])
    hours_dates = pd.to_datetime(pd.read_parquet(MART["paid_hours"])["date"])
    if prod_dates.empty or hours_dates.empty:
        log.warning("Coverage filter: one source is empty, skipping.")
        return df

    prod_min,  prod_max  = prod_dates.min(),  prod_dates.max()
    hours_min, hours_max = hours_dates.min(), hours_dates.max()

    effective_start = max(prod_min,  hours_min)
    effective_end   = min(prod_max,  hours_max)

    # Snap to ISO-week boundaries (Mon=0 ... Sun=6)
    start_wd = effective_start.weekday()
    first_monday = effective_start if start_wd == 0 \
        else effective_start + pd.Timedelta(days=(7 - start_wd))

    end_wd = effective_end.weekday()
    last_sunday = effective_end if end_wd == 6 \
        else effective_end - pd.Timedelta(days=(end_wd + 1))

    log.info("Coverage window:")
    log.info(f"  Production:  {prod_min.date()} -> {prod_max.date()}")
    log.info(f"  Paid hours:  {hours_min.date()} -> {hours_max.date()}")
    log.info(f"  Effective:   {effective_start.date()} -> {effective_end.date()}")
    log.info(f"  First full week (Mon): {first_monday.date()}")
    log.info(f"  Last full week  (Sun): {last_sunday.date()}")

    if first_monday > last_sunday:
        log.warning("Coverage filter: no full ISO weeks within effective range.")
        return df.iloc[0:0]

    before = len(df)
    df = df.copy()
    df["week_start_date"] = pd.to_datetime(df["week_start_date"])
    df["week_end_date"]   = pd.to_datetime(df["week_end_date"])
    df = df[
        (df["week_start_date"] >= first_monday) &
        (df["week_end_date"]   <= last_sunday)
    ].copy()
    log.info(f"  Filtered {before} -> {len(df)} weekly rows (full-coverage weeks only)")
    return df


def run() -> bool:
    log.info("=" * 60)
    log.info("COMPUTE WEEKLY  starting")
    log.info("=" * 60)

    if not MART["ole"].exists():
        log.error(f"ole_computed.parquet not found at {MART['ole']} -- run compute.py first.")
        return False

    con = duckdb.connect()
    con.execute(f"CREATE VIEW ole_shifts AS SELECT * FROM read_parquet('{MART['ole']}')")

    weekly_sql = """
    SELECT
        workcell,

        -- ISO week keys
        CAST(EXTRACT(isoyear FROM date) AS INTEGER)         AS iso_year,
        CAST(EXTRACT(week     FROM date) AS INTEGER)        AS iso_week,

        -- Human-readable label e.g. "2025-W03"
        CONCAT(
            CAST(EXTRACT(isoyear FROM date) AS VARCHAR),
            '-W',
            LPAD(CAST(EXTRACT(week FROM date) AS VARCHAR), 2, '0')
        )                                                   AS week_label,

        -- Week boundaries (Monday to Sunday) -- also in GROUP BY
        DATE_TRUNC('week', date)::DATE                      AS week_start_date,
        (DATE_TRUNC('week', date) + INTERVAL '6 days')::DATE AS week_end_date,

        -- Stage (stable per workcell -- just take first non-null)
        FIRST(stage_label)                                  AS stage_label,
        FIRST(scan_stage)                                   AS scan_stage,

        -- Volume
        SUM(total_qty)                                      AS total_qty,
        COUNT(*)                                            AS shift_count,

        -- Output SMH (summed across shifts)
        ROUND(SUM(effective_output_smh), 4)                 AS total_output_smh,

        -- Input hours (summed across shifts)
        ROUND(SUM(total_input_hours), 4)                    AS total_input_hours,

        -- Headcount (averaged across shifts -- HC is a rate, not a sum)
        ROUND(AVG(hc_direct),  2)                           AS avg_hc_direct,

        -- VA / NVA hours (summed across shifts -- for man-hours distribution)
        ROUND(SUM(va_hours),  4)                            AS total_va_hours,
        ROUND(SUM(nva_hours), 4)                            AS total_nva_hours,

        -- Weekly OLE: computed from weekly aggregates (correct method).
        -- Avoids averaging-of-averages distortion from mean(shift OLE%).
        CASE
            WHEN SUM(total_input_hours) = 0 THEN NULL
            ELSE ROUND(
                (SUM(effective_output_smh) / SUM(total_input_hours)) * 100,
                2
            )
        END                                                 AS ole_pct,

        -- Average of individual shift OLE% (kept for comparison / debugging)
        ROUND(AVG(CASE WHEN ole_pct IS NOT NULL THEN ole_pct END), 2)
                                                            AS ole_pct_avg_shifts,

        -- Data quality breakdown
        COUNT(CASE WHEN data_quality = 'OK'  THEN 1 END)   AS shifts_ok,
        COUNT(CASE WHEN data_quality != 'OK' THEN 1 END)   AS shifts_flagged,

        -- Weighted average SMH coverage (weighted by shift qty)
        ROUND(
            SUM(smh_coverage_pct * total_qty) / NULLIF(SUM(total_qty), 0),
            1
        )                                                   AS smh_coverage_pct

    FROM ole_shifts
    GROUP BY
        workcell,
        EXTRACT(isoyear FROM date),
        EXTRACT(week    FROM date),
        DATE_TRUNC('week', date)::DATE,
        (DATE_TRUNC('week', date) + INTERVAL '6 days')::DATE
    ORDER BY
        workcell,
        iso_year,
        iso_week
    """

    df = con.execute(weekly_sql).df()
    con.close()

    if df.empty:
        log.error("Weekly aggregation returned no rows -- check ole_computed.parquet.")
        return False

    # ─── Full-week coverage filter ────────────────────────────────────────────
    # Drop weeks where EITHER production or paid_hours doesn't fully cover the
    # whole ISO week (Mon-Sun). Computed dynamically from the raw mart so it
    # tracks the available data as it ages in/out, no hardcoded cutoffs.
    df = _filter_full_coverage_weeks(df)

    if df.empty:
        log.error("No full-coverage weeks remain after filter -- check input data ranges.")
        return False

    df.to_parquet(MART["ole_weekly"], index=False)

    # -- Summary log
    log.info(f"ole_weekly.parquet -> {len(df)} rows")

    summary = (
        df.groupby("workcell")
        .agg(
            total_weeks=("week_label", "count"),
            from_week=("week_label", "first"),
            to_week=("week_label", "last"),
            avg_ole_pct=("ole_pct", "mean"),
            min_ole_pct=("ole_pct", "min"),
            max_ole_pct=("ole_pct", "max"),
        )
        .round({"avg_ole_pct": 2, "min_ole_pct": 2, "max_ole_pct": 2})
    )
    log.info("\n" + summary.to_string())
    log.info("COMPUTE WEEKLY  complete")
    return True


if __name__ == "__main__":
    run()