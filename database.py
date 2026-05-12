"""
database.py
───────────
SQLite database for user-entered operational data.

Tables:
  downtime_logs   — supervisor-keyed production interruptions
  transfer_logs   — cross-workcell man-hour transfers

This is separate from the parquet mart (which is computed/read-only).
The SQLite file lives at data/operational.db and persists across restarts.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "operational.db"


def get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")  # safe concurrent reads
    return conn


def init_db():
    """Create tables if they don't exist. Safe to call on every startup."""
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS downtime_logs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
                date        TEXT    NOT NULL,   -- YYYY-MM-DD
                shift       INTEGER NOT NULL,   -- 1=Day  2=Night  3=Overtime
                workcell    TEXT    NOT NULL,   -- matches WORKCELL_CONFIG key
                bay         TEXT,
                dept        TEXT    NOT NULL,
                code        TEXT    NOT NULL,
                dl_affected INTEGER NOT NULL DEFAULT 0,
                minutes     INTEGER NOT NULL,
                commentary  TEXT
            );

            CREATE TABLE IF NOT EXISTS transfer_logs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
                date        TEXT    NOT NULL,   -- YYYY-MM-DD
                shift       INTEGER NOT NULL,   -- 1=Day  2=Night  3=Overtime
                from_wc     TEXT    NOT NULL,   -- source workcell
                to_wc       TEXT    NOT NULL,   -- destination workcell
                va_hc       INTEGER NOT NULL DEFAULT 0,
                va_hrs      REAL    NOT NULL DEFAULT 0,
                nva_hc      INTEGER NOT NULL DEFAULT 0,
                nva_hrs     REAL    NOT NULL DEFAULT 0
            );
        """)
