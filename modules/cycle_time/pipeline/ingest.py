"""
ingest.py  (cycle_time)
───────────────────────
Pulls raw process data from IEDB3.0 API for all 41 active Penang customers
and writes/updates raw.parquet.

One row per (assembly, revision, sub_workcenter, process, customer).

Modes:
  incremental  — sets BeginDate = last_run_date from state file.
                 Only fetches records updated since last run.
                 Upserts into existing raw.parquet.
  full         — no date filter, fetches everything, overwrites raw.parquet.
"""

import json
import logging
import re
from datetime import datetime

import pandas as pd

from modules.cycle_time.client import fetch_all_pages
from modules.cycle_time.config import CT_CUSTOMERS, CT_MART, CT_MART_DIR, CT_STATE_FILE

log = logging.getLogger(__name__)

# ─── Column name normalisation ────────────────────────────────────────────────
# API returns camelCase JSON keys → convert to snake_case for parquet storage.

def _camel_to_snake(name: str) -> str:
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


# ─── State helpers ────────────────────────────────────────────────────────────

def _load_state() -> dict:
    if not CT_STATE_FILE.exists():
        return {}
    try:
        with open(CT_STATE_FILE) as f:
            return json.load(f)
    except Exception as e:
        log.warning(f"Could not read CT state ({e}); starting fresh.")
        return {}


def _save_state(state: dict) -> None:
    try:
        with open(CT_STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        log.error(f"Could not write CT state: {e}")


# ─── Upsert helpers ───────────────────────────────────────────────────────────

# Primary key for deduplication / upsert
_UPSERT_KEYS = ["assembly", "revision", "sub_workcenter", "process", "customer"]


def _upsert(existing: pd.DataFrame, new: pd.DataFrame) -> pd.DataFrame:
    """
    Replace existing rows whose primary key appears in new_df, then append new rows.
    Effectively an upsert: newer API data wins for any overlapping keys.
    """
    if existing.empty:
        return new
    if new.empty:
        return existing

    # Only drop rows whose key combination exists in new_df
    key_cols = [k for k in _UPSERT_KEYS if k in existing.columns and k in new.columns]
    new_keys = set(map(tuple, new[key_cols].values.tolist()))
    keep_mask = ~existing[key_cols].apply(tuple, axis=1).isin(new_keys)
    kept = existing[keep_mask]

    merged = pd.concat([kept, new], ignore_index=True)
    log.info(
        f"  Upsert: kept {len(kept)} existing rows + {len(new)} new/updated = {len(merged)} total"
    )
    return merged


# ─── Core ingest ──────────────────────────────────────────────────────────────

def _fetch_customer(
    customer: str,
    division: str,
    begin_date: str | None,
) -> pd.DataFrame:
    log.info(f"  → {customer} ({division})")
    records = fetch_all_pages(customer, division, begin_date=begin_date)
    if not records:
        log.info(f"      no records returned")
        return pd.DataFrame()

    df = pd.DataFrame(records)
    # Normalise column names camelCase → snake_case
    df.columns = [_camel_to_snake(c) for c in df.columns]
    # Tag with customer/division so we know the source in the parquet
    df["_customer"] = customer
    df["_division"] = division
    log.info(f"      {len(df)} records")
    return df


def run(mode: str = "incremental", progress_cb=None,
        only: list[str] | None = None, exclude: list[str] | None = None) -> bool:
    """
    progress_cb: optional callable(customer_name, customers_done, customers_total)
                 invoked AFTER each customer is fetched (success or fail).
                 Used by the FastAPI router to surface progress to FE.
    only:        if given, only fetch these customer names (case-insensitive).
    exclude:     if given, skip these customer names (case-insensitive).
                 `only` wins over `exclude` when both are set.
    """
    log.info("=" * 60)
    log.info(f"CYCLE TIME INGEST  starting  (mode={mode})")
    log.info("=" * 60)

    CT_MART_DIR.mkdir(parents=True, exist_ok=True)

    state = _load_state() if mode == "incremental" else {}
    begin_date: str | None = state.get("last_run_date") if mode == "incremental" else None

    if begin_date:
        log.info(f"Incremental: fetching records updated since {begin_date}")
    else:
        log.info("Full fetch: no date filter (all records)")

    # Filter customer list by --only / --exclude.
    only_set    = {c.lower() for c in only}    if only    else None
    exclude_set = {c.lower() for c in exclude} if exclude else None
    customers = [
        c for c in CT_CUSTOMERS
        if (only_set is None or c["customer"].lower() in only_set)
        and (exclude_set is None or c["customer"].lower() not in exclude_set)
    ]
    if only:    log.info(f"Filter --only:    {only}    → {len(customers)} customer(s) selected")
    if exclude: log.info(f"Filter --exclude: {exclude} → {len(customers)} customer(s) remaining")

    frames: list[pd.DataFrame] = []
    failed: list[str] = []
    total = len(customers)

    for i, cust in enumerate(customers, start=1):
        if progress_cb:
            try:
                progress_cb(cust["customer"], i - 1, total)
            except Exception:
                pass
        try:
            df = _fetch_customer(cust["customer"], cust["division"], begin_date)
            if not df.empty:
                frames.append(df)
        except Exception as e:
            log.error(f"  FAILED {cust['customer']}: {e}")
            failed.append(cust["customer"])
        if progress_cb:
            try:
                progress_cb(None, i, total)
            except Exception:
                pass

    if not frames:
        log.warning("No data fetched from any customer.")
        if failed:
            log.error(f"Failed customers: {failed}")
        return False

    new_df = pd.concat(frames, ignore_index=True)
    log.info(f"Fetched {len(new_df)} total rows across {len(frames)} customers")

    # Merge with existing parquet
    if mode == "incremental" and CT_MART["raw"].exists():
        try:
            existing = pd.read_parquet(CT_MART["raw"])
            final_df = _upsert(existing, new_df)
        except Exception as e:
            log.warning(f"Could not read existing raw.parquet ({e}); overwriting.")
            final_df = new_df
    else:
        final_df = new_df

    final_df.to_parquet(CT_MART["raw"], index=False)
    log.info(f"raw.parquet written: {len(final_df)} rows → {CT_MART['raw']}")

    # Persist state
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    state.update({
        "last_run_date":      now,
        "last_run_mode":      mode,
        "total_rows":         len(final_df),
        "failed_customers":   failed,
        "customers_fetched":  len(frames),
    })
    _save_state(state)

    if failed:
        log.warning(f"Completed with failures: {failed}")
    log.info("CYCLE TIME INGEST  complete")
    return True
