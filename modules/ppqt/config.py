"""
modules/ppqt/config.py
──────────────────────
PPQT module configuration. Placeholder — overwrite with real settings
when the module is built out.

Mirrors the shape of modules/ole/config.py and modules/cycle_time/config.py
so the pattern is consistent across modules.
"""

from core.paths import DATA_MART_DIR

# ─── Mart filenames ───────────────────────────────────────────────────────────
PPQT_MART_DIR = DATA_MART_DIR / "ppqt"
PPQT_MART_DIR.mkdir(parents=True, exist_ok=True)

PPQT_MART = {
    # Replace with real parquet names when the pipeline lands.
    "raw":     PPQT_MART_DIR / "raw.parquet",
    "summary": PPQT_MART_DIR / "summary.parquet",
}
