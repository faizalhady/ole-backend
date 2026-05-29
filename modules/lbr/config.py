"""
modules/lbr/config.py
─────────────────────
LBR module configuration. Placeholder — overwrite with real settings
when the module is built out.
"""

from core.paths import DATA_MART_DIR

LBR_MART_DIR = DATA_MART_DIR / "lbr"
LBR_MART_DIR.mkdir(parents=True, exist_ok=True)

LBR_MART = {
    "raw":     LBR_MART_DIR / "raw.parquet",
    "summary": LBR_MART_DIR / "summary.parquet",
}
