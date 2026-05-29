"""
transform.py  (cycle_time)
──────────────────────────
Reads raw.parquet (one row per assembly/revision/sub_workcenter/process)
and pivots it into pivoted.parquet — one row per assembly/revision/sub_workcenter
with each process (BIRTH, SCRB, GLUEB, …) as its own column.

This matches the exact table layout shown in Image 2.
"""

import logging

import pandas as pd

from modules.cycle_time.config import CT_MART

log = logging.getLogger(__name__)

# ─── Pivot identity columns ───────────────────────────────────────────────────
# These stay as rows (not pivoted). Everything else is metadata or pivoted.
# IMPORTANT: do NOT include process-level fields here (grp, playbook, priority,
# order, alias, hc, etc.) — they vary per process and would prevent the pivot
# from collapsing rows. Only fields that are constant for an
# (assembly, revision, sub_workcenter) belong in the index.
_INDEX_COLS = [
    "customer",
    "division",
    "family",
    "assembly",
    "revision",
    "workcenter",
    "workcenter_type",
    "sub_workcenter",
]

# The friendly, line-specific process name (e.g. "MA 1", "HI-PORT", "BURN IN")
# lives in the API's `Alias` field — which is what the customer-facing Excel
# reports use. The raw `Process` field carries generic codes ("Assembly 1",
# "Hi-Pot 1") that aren't meaningful to engineers. We pivot on Alias so the
# pivoted.parquet column headers match the Excel report.
_PROCESS_COL   = "alias"
_VALUE_COL     = "cycle_time_per_process"


def run() -> bool:
    log.info("=" * 60)
    log.info("CYCLE TIME TRANSFORM  starting")
    log.info("=" * 60)

    if not CT_MART["raw"].exists():
        log.error(f"raw.parquet not found at {CT_MART['raw']}. Run ingest first.")
        return False

    try:
        df = pd.read_parquet(CT_MART["raw"])
    except Exception as e:
        log.error(f"Could not read raw.parquet: {e}")
        return False

    log.info(f"Raw rows: {len(df)}")

    # ── Guard: required columns ───────────────────────────────────────────────
    required = [_PROCESS_COL, _VALUE_COL]
    missing = [c for c in required if c not in df.columns]
    if missing:
        log.error(f"Missing columns in raw.parquet: {missing}")
        log.error(f"Available columns: {list(df.columns)}")
        return False

    # ── Only keep index cols that actually exist in the data ──────────────────
    index_cols = [c for c in _INDEX_COLS if c in df.columns]

    # ── Ensure numeric value col ──────────────────────────────────────────────
    df[_VALUE_COL] = pd.to_numeric(df[_VALUE_COL], errors="coerce")

    # ── Pivot: process rows → columns ─────────────────────────────────────────
    # aggfunc='first': if an assembly/sub_wc/process combination appears more than
    # once (e.g. duplicate entries), take the first occurrence.
    try:
        pivoted = df.pivot_table(
            index=index_cols,
            columns=_PROCESS_COL,
            values=_VALUE_COL,
            aggfunc="first",
        ).reset_index()
        pivoted.columns.name = None          # remove "process" label from column axis
    except Exception as e:
        log.error(f"Pivot failed: {e}")
        return False

    process_cols = [c for c in pivoted.columns if c not in index_cols]
    log.info(f"Pivoted: {len(pivoted)} rows | {len(process_cols)} process columns")
    log.info(f"Process columns found: {sorted(process_cols)}")

    # ── Write ─────────────────────────────────────────────────────────────────
    pivoted.to_parquet(CT_MART["pivoted"], index=False)
    log.info(f"pivoted.parquet written → {CT_MART['pivoted']}")
    log.info("CYCLE TIME TRANSFORM  complete")
    return True
