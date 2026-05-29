"""
refresh.py  (cycle_time)
────────────────────────
Single entry point for the Cycle Time pipeline.

  python -m modules.cycle_time.pipeline.refresh                                    # incremental
  python -m modules.cycle_time.pipeline.refresh --full                             # full re-fetch
  python -m modules.cycle_time.pipeline.refresh --full --exclude KEYSIGHT          # 40 customers
  python -m modules.cycle_time.pipeline.refresh --full --only   KEYSIGHT           # just KEYSIGHT
  python -m modules.cycle_time.pipeline.refresh --full --exclude KEYSIGHT,ARISTANETWORKS,Tellabs

Steps:
  1. ingest    — fetch from IEDB3.0 API → raw.parquet
  2. transform — pivot raw → pivoted.parquet (Image 2 layout)
"""

import sys
import argparse
import logging
from datetime import datetime
from pathlib import Path

# Allow running as a script from the project root
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from modules.cycle_time.pipeline.ingest    import run as run_ingest
from modules.cycle_time.pipeline.transform import run as run_transform

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
log = logging.getLogger(__name__)


def run(mode: str = "incremental",
        only: list[str] | None = None,
        exclude: list[str] | None = None) -> bool:
    start = datetime.now()
    title = "INCREMENTAL" if mode == "incremental" else "FULL"

    log.info("╔══════════════════════════════════════════════════════════╗")
    log.info(f"║        CYCLE TIME PIPELINE  —  {title:<28s}║")
    log.info("╚══════════════════════════════════════════════════════════╝")
    log.info(f"Started at {start.strftime('%Y-%m-%d %H:%M:%S')}")

    if not run_ingest(mode=mode, only=only, exclude=exclude):
        log.error("Ingest failed — pipeline aborted.")
        return False

    if not run_transform():
        log.error("Transform failed — pivoted.parquet not written.")
        return False

    elapsed = (datetime.now() - start).total_seconds()
    log.info(f"Cycle Time pipeline complete in {elapsed:.1f}s")
    return True


def _csv(s: str) -> list[str]:
    return [x.strip() for x in s.split(",") if x.strip()]


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Cycle Time pipeline refresh")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--incremental", action="store_const", const="incremental", dest="mode",
                   help="Fetch only records updated since last run (default)")
    g.add_argument("--full",        action="store_const", const="full",        dest="mode",
                   help="Full re-fetch — overwrites raw.parquet")
    p.set_defaults(mode="incremental")

    customer_group = p.add_mutually_exclusive_group()
    customer_group.add_argument("--only",    type=_csv, default=None,
                                help="Only ingest these customers (comma-separated, case-insensitive)")
    customer_group.add_argument("--exclude", type=_csv, default=None,
                                help="Skip these customers (comma-separated, case-insensitive)")

    args = p.parse_args()
    success = run(mode=args.mode, only=args.only, exclude=args.exclude)
    sys.exit(0 if success else 1)
