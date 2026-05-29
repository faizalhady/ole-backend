"""
core/paths.py
─────────────
Single source of truth for project paths. Every module that needs to
resolve a file under the repo (data/, scripts/, etc.) imports from here
so that moving files around doesn't break `Path(__file__).parent` math.
"""

from pathlib import Path

PROJECT_ROOT  = Path(__file__).resolve().parents[1]
DATA_DIR      = PROJECT_ROOT / "data"
DATA_RAW_DIR  = DATA_DIR / "raw"
DATA_MART_DIR = DATA_DIR / "mart"
