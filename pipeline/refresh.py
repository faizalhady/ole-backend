"""
refresh.py
──────────
Single entry point. Run this to refresh all mart data end-to-end.

  python pipeline/refresh.py

Steps
  1. ingest  — load raw sources, normalise, write Parquet
  2. compute — DuckDB JOIN + OLE calculation, write ole_computed.parquet
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
from datetime import datetime

from pipeline.ingest        import run as run_ingest
from pipeline.compute       import run as run_compute
from pipeline.compute_weekly import run as run_compute_weekly

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
log = logging.getLogger(__name__)


def run():
    start = datetime.now()
    log.info("╔══════════════════════════════════════════════════════════╗")
    log.info("║              OLE PIPELINE  —  FULL REFRESH               ║")
    log.info("╚══════════════════════════════════════════════════════════╝")
    log.info(f"Started at {start.strftime('%Y-%m-%d %H:%M:%S')}")

    ok = run_ingest()
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

    elapsed = (datetime.now() - start).total_seconds()
    log.info(f"Pipeline complete in {elapsed:.1f}s")


if __name__ == "__main__":
    run()
