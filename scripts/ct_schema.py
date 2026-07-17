"""ct_schema.py — dump parquet column sets for the cycle_time mart.
Metadata-only read (fast, no data load). Run on BOTH machines, diff the output.

  python ct_schema.py                 # uses ./ (or edit MART below)
  python ct_schema.py <mart_dir>
"""
import sys
from pathlib import Path
import pyarrow.parquet as pq

MART = Path(sys.argv[1] if len(sys.argv) > 1 else ".")

for f in sorted(MART.glob("*.parquet")):
    schema = pq.read_schema(f)                 # metadata only
    cols = list(schema.names)
    print(f"\n== {f.name}  ({len(cols)} cols) ==")
    print(", ".join(cols))
