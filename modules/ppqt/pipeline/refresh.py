"""
modules/ppqt/pipeline/refresh.py
────────────────────────────────
PPQT pipeline entry point. Placeholder — overwrite with real ingest/transform
when the module is built out.

Convention (matches OLE + Cycle Time):
  python -m modules.ppqt.pipeline.refresh                 # incremental
  python -m modules.ppqt.pipeline.refresh --full          # full reload
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import argparse
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
log = logging.getLogger(__name__)


def run(mode: str = "incremental") -> bool:
    """Placeholder pipeline. Replace with real ingest + transform calls."""
    log.info(f"PPQT pipeline placeholder invoked (mode={mode}) — nothing to do yet")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true", help="Full reload (default: incremental)")
    args = parser.parse_args()
    mode = "full" if args.full else "incremental"
    ok = run(mode=mode)
    sys.exit(0 if ok else 1)
