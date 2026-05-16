"""
refresh.py
──────────
Single entry point. Run this to refresh all mart data end-to-end.

  python pipeline/refresh.py                  # incremental (default — safe)
  python pipeline/refresh.py --incremental    # same as above (explicit)
  python pipeline/refresh.py --full           # nuke & re-read everything

Modes
  incremental — only reads CSV files newer than the last successful run.
                Appends to existing parquet marts. PRESERVES historical
                rows that have been deleted from the network share by
                retention. Use this for routine / scheduled runs.

  full        — re-reads everything currently visible in the network share
                and overwrites marts. Anything no longer in the share
                is LOST. Use only for disaster recovery / schema migration.

Steps
  1. ingest  — load raw sources, normalise, write Parquet
  2. compute — DuckDB JOIN + OLE calculation, write ole_computed.parquet
  3. weekly  — ISO-week aggregation, write ole_weekly.parquet
  4. mh      — per-shift man-hours distribution, write mh_distribution.parquet
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import argparse
import logging
from datetime import datetime

from pipeline.ingest         import run as run_ingest
from pipeline.compute        import run as run_compute
from pipeline.compute_weekly import run as run_compute_weekly
from pipeline.compute_mh     import run as run_compute_mh

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
log = logging.getLogger(__name__)


def run(mode: str = "incremental"):
    start = datetime.now()
    title = "INCREMENTAL REFRESH" if mode == "incremental" else "FULL REFRESH"
    log.info("╔══════════════════════════════════════════════════════════╗")
    log.info(f"║              OLE PIPELINE  —  {title:<28s}║")
    log.info("╚══════════════════════════════════════════════════════════╝")
    log.info(f"Started at {start.strftime('%Y-%m-%d %H:%M:%S')}")

    ok = run_ingest(mode=mode)
    if not ok:
        log.error("Ingest failed — pipeline aborted.")
        sys.exit(1)

    ok = run_compute()
    if not ok:
        log.error("Compute failed — mart may be incomplete.")
        sys.exit(1)

    ok = run_compute_weekly()
    if not ok:
        log.error("Weekly compute failed — ole_weekly.parquet not written.")
        sys.exit(1)

    ok = run_compute_mh()
    if not ok:
        log.error("MH-distribution compute failed — mh_distribution.parquet not written.")
        sys.exit(1)

    elapsed = (datetime.now() - start).total_seconds()
    log.info(f"Pipeline complete in {elapsed:.1f}s")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="OLE pipeline refresh")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--incremental", action="store_const", const="incremental", dest="mode",
                   help="Append new files to existing mart (default — preserves historical data)")
    g.add_argument("--full",        action="store_const", const="full",        dest="mode",
                   help="Re-read everything currently in the share, overwriting marts")
    p.set_defaults(mode="incremental")
    args = p.parse_args()
    run(mode=args.mode)
