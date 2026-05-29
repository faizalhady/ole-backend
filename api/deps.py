"""
api/deps.py
───────────
Shared helpers used across OLE-side routers. Cycle Time and any other
self-contained modules should NOT import from here — they own their
own helpers (kept duplication intentional to preserve module isolation).
"""

import math

import duckdb
import pandas as pd
from fastapi import HTTPException

from modules.ole.config import MART, WORKCELL_CONFIG


# ─── Shift constants (single source of truth) ─────────────────────────────────
# 1 = Normal   2 = Night   3 = Day
SHIFT_LABELS = {1: "Normal", 2: "Night", 3: "Day"}


def con():
    """Fresh in-memory DuckDB connection (no shared state across requests)."""
    return duckdb.connect()


def parquet(c, key, alias=None):
    """Register an OLE mart parquet as a DuckDB view. 503 if missing."""
    path = MART[key]
    if not path.exists():
        raise HTTPException(
            status_code=503,
            detail=f"Mart file not found: {path.name}. Run /api/refresh first.",
        )
    view_name = alias or key.replace("-", "_")
    c.execute(f"CREATE VIEW {view_name} AS SELECT * FROM read_parquet('{path}')")


def df_to_json(df):
    """Pandas DataFrame → list[dict], cleaning NaNs and converting numpy/timestamp types."""
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


def where_clause(workcell=None, date_from=None, date_to=None, date_col="date", plant=None):
    """Build a WHERE clause for OLE mart queries from common filter params."""
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


def row_to_dict(row) -> dict:
    """Convert sqlite3.Row to plain dict."""
    return dict(row)
