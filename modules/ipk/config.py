"""
modules/ipk/config.py
─────────────────────
IPK module configuration. Placeholder — overwrite with real settings
when the module is built out.
"""

from core.paths import DATA_MART_DIR

IPK_MART_DIR = DATA_MART_DIR / "ipk"
IPK_MART_DIR.mkdir(parents=True, exist_ok=True)

IPK_MART = {
    "raw":     IPK_MART_DIR / "raw.parquet",
    "summary": IPK_MART_DIR / "summary.parquet",
}
