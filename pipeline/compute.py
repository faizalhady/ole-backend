"""
compute.py
──────────
Reads the clean Parquet files from the mart, performs DuckDB JOINs,
computes OLE per workcell per date per shift, and writes ole_computed.parquet.

OLE formula (matches existing OLE web tool):
  Numerator   = SUM(qty x smh_value)   [per workcell, date, shift]
  Denominator = SUM(tph_direct)         [per workcell, date, shift, ALL rows]
  OLE %       = (Numerator / Denominator) x 100

IMPORTANT: PEN_PaidHours_Raw_* TPHDirect already contains direct + support hours
combined per employee row. SUM all rows (VA, NVA, blank) — do NOT filter by
value_type for the denominator. value_type is only used for VA/NVA split display.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
import duckdb
import pandas as pd

from config import MART, WORKCELL_CONFIG

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
log = logging.getLogger(__name__)


def run() -> bool:
    log.info("=" * 60)
    log.info("COMPUTE  starting")
    log.info("=" * 60)

    for key in ["production", "paid_hours", "smh"]:
        if not MART[key].exists():
            log.error(f"Mart file missing: {MART[key]} -- run ingest first.")
            return False

    con = duckdb.connect()

    con.execute(f"CREATE VIEW production AS SELECT * FROM read_parquet('{MART['production']}')")
    con.execute(f"CREATE VIEW paid_hours AS SELECT * FROM read_parquet('{MART['paid_hours']}')")
    con.execute(f"CREATE VIEW smh_lookup AS SELECT * FROM read_parquet('{MART['smh']}')")
    log.info("Parquet views created")

    # ── Step 1: Output SMH per workcell / date / shift ────────────────────────
    con.execute("""
    CREATE TEMP TABLE output_smh AS
    SELECT
        p.workcell,
        p.date,
        p.shift,
        COUNT(DISTINCT p.assembly)                              AS assembly_count,
        SUM(p.qty)                                             AS total_qty,
        SUM(CASE WHEN s.smh_value > 0
                 THEN p.qty * s.smh_value ELSE 0 END)          AS effective_output_smh,
        SUM(CASE WHEN s.smh_value IS NULL OR s.smh_value = 0
                 THEN p.qty ELSE 0 END)                        AS qty_missing_smh,
        COUNT(DISTINCT CASE WHEN s.smh_value IS NULL
                            OR s.smh_value = 0
                            THEN p.assembly END)               AS assemblies_missing_smh
    FROM production p
    LEFT JOIN smh_lookup s
           ON p.workcell = s.workcell
          AND p.assembly = s.assembly
    GROUP BY p.workcell, p.date, p.shift
    """)
    log.info("Step 1 complete -- output SMH computed")

    # ── Step 2: Aggregate input hours per workcell / date / shift ─────────────
    # SUM all tph_direct rows regardless of value_type (VA/NVA/blank).
    # The raw paid hours file stores combined hours per employee in tph_direct —
    # filtering by value_type would DROP rows and undercount the denominator.
    # value_type is only used for VA/NVA split display, NOT for OLE calculation.
    con.execute("""
    CREATE TEMP TABLE input_hours AS
    SELECT
        workcell,
        date,
        shift,
        COUNT(*)                                                AS headcount,
        SUM(thc_direct)                                         AS total_hc_direct,
        SUM(tph_direct)                                         AS total_input_hours,
        SUM(CASE WHEN value_type = 'VA'  THEN tph_direct ELSE 0 END) AS va_hours,
        SUM(CASE WHEN value_type = 'NVA' OR value_type = '' THEN tph_direct ELSE 0 END) AS nva_hours
    FROM paid_hours
    GROUP BY workcell, date, shift
    """)
    log.info("Step 2 complete -- input hours aggregated (ALL rows summed)")

    # ── Step 3: JOIN and compute OLE ──────────────────────────────────────────
    con.execute("""
    CREATE TEMP TABLE ole_result AS
    SELECT
        o.workcell,
        o.date,
        o.shift,

        s_meta.stage_label,
        s_meta.scan_stage,

        -- output side
        o.assembly_count,
        o.total_qty,
        ROUND(o.effective_output_smh, 4)                        AS effective_output_smh,
        o.qty_missing_smh,
        o.assemblies_missing_smh,

        -- input side
        COALESCE(h.total_hc_direct,   0)                        AS hc_direct,
        COALESCE(h.total_input_hours, 0)                        AS total_input_hours,

        -- VA / NVA breakdown (display only, not used in OLE calculation)
        COALESCE(h.va_hours,          0)                        AS va_hours,
        COALESCE(h.nva_hours,         0)                        AS nva_hours,

        -- OLE calculation
        CASE
            WHEN COALESCE(h.total_input_hours, 0) = 0 THEN NULL
            ELSE ROUND(
                (o.effective_output_smh / h.total_input_hours) * 100, 2
            )
        END                                                      AS ole_pct,

        -- Data quality flag
        CASE
            WHEN COALESCE(h.total_input_hours, 0) = 0 THEN 'NO_INPUT_HOURS'
            WHEN o.effective_output_smh = 0            THEN 'NO_OUTPUT_SMH'
            WHEN o.qty_missing_smh > 0                 THEN 'PARTIAL_SMH'
            ELSE 'OK'
        END                                                      AS data_quality

    FROM output_smh o

    LEFT JOIN input_hours h
           ON o.workcell = h.workcell
          AND o.date     = h.date
          AND o.shift    = h.shift

    LEFT JOIN (
        SELECT DISTINCT workcell, stage_label, scan_stage
        FROM smh_lookup
    ) s_meta ON o.workcell = s_meta.workcell

    ORDER BY o.workcell, o.date, o.shift
    """)
    log.info("Step 3 complete -- OLE computed")

    # ── Step 4: SMH coverage per assembly ─────────────────────────────────────
    con.execute(f"""
    CREATE TEMP TABLE smh_assembly_status AS
    SELECT
        p.workcell,
        p.assembly,
        COALESCE(s.smh_value, 0)                                AS smh_value,
        SUM(p.qty)                                              AS total_qty_produced,
        MIN(p.date)                                             AS first_seen_date,
        MAX(p.date)                                             AS last_seen_date,
        COUNT(DISTINCT p.date)                                  AS active_days,
        CASE
            WHEN s.assembly IS NULL  THEN 'NOT_IN_SMH_DB'
            WHEN s.smh_value = 0     THEN 'MISSING_SMH'
            ELSE                          'OK'
        END                                                     AS smh_status
    FROM read_parquet('{MART["production"]}') p
    LEFT JOIN read_parquet('{MART["smh"]}') s
           ON p.workcell = s.workcell
          AND p.assembly = s.assembly
    GROUP BY p.workcell, p.assembly, s.assembly, s.smh_value
    ORDER BY p.workcell, smh_status, total_qty_produced DESC
    """)
    log.info("Step 4 complete -- SMH assembly coverage computed")

    # ── Export ────────────────────────────────────────────────────────────────
    result = con.execute("SELECT * FROM ole_result").df()

    result["smh_coverage_pct"] = (
        (result["total_qty"] - result["qty_missing_smh"])
        / result["total_qty"].replace(0, float("nan"))
        * 100
    ).round(1)

    result.to_parquet(MART["ole"], index=False)

    smh_status = con.execute("SELECT * FROM smh_assembly_status").df()
    smh_status.to_parquet(MART["smh_status"], index=False)

    # ── Summary log ───────────────────────────────────────────────────────────
    log.info(f"OLE result:  {len(result)} rows written to ole_computed.parquet")
    log.info(f"SMH status:  {len(smh_status)} assembly rows written to smh_assembly_status.parquet")

    summary = con.execute("""
        SELECT
            workcell, scan_stage,
            COUNT(*)                    AS shifts,
            ROUND(AVG(ole_pct), 2)      AS avg_ole_pct,
            ROUND(MIN(ole_pct), 2)      AS min_ole_pct,
            ROUND(MAX(ole_pct), 2)      AS max_ole_pct,
            ROUND(SUM(effective_output_smh), 1) AS total_output_smh,
            ROUND(SUM(total_input_hours), 1)    AS total_input_hours,
            COUNT(CASE WHEN data_quality != 'OK' THEN 1 END) AS flagged_shifts
        FROM ole_result
        GROUP BY workcell, scan_stage
        ORDER BY workcell
    """).df()

    smh_summary = con.execute("""
        SELECT workcell, smh_status,
               COUNT(*) AS assemblies,
               SUM(total_qty_produced) AS qty_produced
        FROM smh_assembly_status
        GROUP BY workcell, smh_status
        ORDER BY workcell, smh_status
    """).df()

    log.info("\n" + summary.to_string(index=False))
    log.info("\nSMH coverage breakdown:\n" + smh_summary.to_string(index=False))
    log.info("COMPUTE  complete")

    con.close()
    return True


if __name__ == "__main__":
    run()
