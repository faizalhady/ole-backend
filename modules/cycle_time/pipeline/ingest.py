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
import shutil
from datetime import datetime
from pathlib import Path

import pandas as pd

from modules.cycle_time.client import fetch_all_pages, fetch_page
from modules.cycle_time.config import CT_CUSTOMERS, CT_MART, CT_MART_DIR, CT_STATE_FILE, PAGE_SIZE

log = logging.getLogger(__name__)

# ─── Per-customer shard layout ────────────────────────────────────────────────
# Each customer writes pages to its own folder; the page parquet is the unit
# of durable progress. Crash / timeout mid-customer keeps all completed pages.
#
#   data/mart/cycle_time/raw_shards/
#     ASP/
#       page_0001.parquet
#       page_0002.parquet
#       ...
#       .state.json     { "last_completed_page": N, "total_count": T, "complete": true|false, "rows": M }
#
# At the end of run(), all complete shards are concatenated into raw.parquet.
SHARDS_DIR = CT_MART_DIR / "raw_shards"

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

def _customer_slug(customer: str) -> str:
    """Filesystem-safe shard directory name."""
    return re.sub(r"[^A-Za-z0-9_-]+", "_", customer).strip("_")


def _shard_state_path(customer: str) -> Path:
    return SHARDS_DIR / _customer_slug(customer) / ".state.json"


def _load_shard_state(customer: str) -> dict:
    p = _shard_state_path(customer)
    if not p.exists():
        return {"last_completed_page": 0, "total_count": None, "complete": False, "rows": 0}
    try:
        return json.loads(p.read_text())
    except Exception as e:
        log.warning(f"  Shard state unreadable for {customer} ({e}) — starting fresh")
        return {"last_completed_page": 0, "total_count": None, "complete": False, "rows": 0}


def _save_shard_state(customer: str, state: dict) -> None:
    p = _shard_state_path(customer)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, indent=2))


def _normalise_page_df(records: list[dict], customer: str, division: str) -> pd.DataFrame:
    """Page records → snake_cased DataFrame with provenance tags."""
    df = pd.DataFrame(records)
    df.columns = [_camel_to_snake(c) for c in df.columns]
    df["_customer"] = customer
    df["_division"] = division
    return df


def _fetch_customer_resumable(
    customer: str,
    division: str,
    begin_date: str | None,
    full: bool,
) -> bool:
    """
    Fetch a customer in resumable per-page chunks.
      - Each page written to raw_shards/{slug}/page_{n:04d}.parquet immediately
      - .state.json updated after each successful page write
      - On --full + no existing shard: fresh fetch
      - On --full + existing shard: WIPED first, then fresh fetch
      - On --incremental: resumes from last_completed_page + 1
      - Returns True if customer fully complete, False on partial (timeout etc.)
    """
    slug = _customer_slug(customer)
    shard_dir = SHARDS_DIR / slug
    state = _load_shard_state(customer)

    # --full wipes COMPLETE shards (force re-fetch) but always resumes
    # PARTIAL shards — we never throw away in-flight pages, even with --full.
    # If you really want to restart a partial, delete the shard folder by hand.
    if full and shard_dir.exists() and state["complete"]:
        log.info(f"  → {customer} ({division})  [--full] wiping completed shard ({state['rows']:,} rows) to re-fetch")
        shutil.rmtree(shard_dir)
        state = {"last_completed_page": 0, "total_count": None, "complete": False, "rows": 0}

    if state["complete"]:
        log.info(f"  → {customer} ({division})  already complete ({state['rows']:,} rows) — skipping")
        return True

    shard_dir.mkdir(parents=True, exist_ok=True)
    start_page = state["last_completed_page"] + 1
    if start_page > 1:
        log.info(f"  → {customer} ({division})  resuming from page {start_page} "
                 f"({state['rows']:,} rows already on disk)")
    else:
        log.info(f"  → {customer} ({division})")

    page = start_page
    rows_added = 0
    while True:
        try:
            batch = fetch_page(customer, division, page, PAGE_SIZE, begin_date)
        except Exception as e:
            log.error(f"      FAILED at page {page}: {e}")
            log.error(f"      kept {state['rows']:,} rows on disk; resume next run")
            return False

        if not batch:
            # Empty page — we're done (no more data).
            state["complete"] = True
            _save_shard_state(customer, state)
            log.info(f"      complete: {state['rows']:,} rows total")
            return True

        # Write the page atomically: write to .tmp then rename.
        df = _normalise_page_df(batch, customer, division)
        page_path = shard_dir / f"page_{page:04d}.parquet"
        tmp_path  = shard_dir / f"page_{page:04d}.parquet.tmp"
        df.to_parquet(tmp_path, index=False)
        tmp_path.replace(page_path)

        # Update state AFTER the page is durable.
        if state["total_count"] is None:
            tc = batch[0].get("totalCount") or batch[0].get("TotalCount")
            if tc is not None:
                state["total_count"] = int(tc)
        state["last_completed_page"] = page
        state["rows"] += len(df)
        _save_shard_state(customer, state)
        rows_added += len(df)

        # Termination: known total reached, or short page.
        if state["total_count"] is not None and state["rows"] >= state["total_count"]:
            state["complete"] = True
            _save_shard_state(customer, state)
            log.info(f"      complete: {state['rows']:,} / {state['total_count']:,} rows")
            return True
        if len(batch) < PAGE_SIZE:
            state["complete"] = True
            _save_shard_state(customer, state)
            log.info(f"      complete: {state['rows']:,} rows (short final page)")
            return True

        # Periodic progress for big customers — every 10 pages.
        if page % 10 == 0:
            tc = state["total_count"]
            pct = f"{state['rows'] / tc * 100:.1f}%" if tc else "?"
            log.info(f"      page {page} done — {state['rows']:,} rows ({pct})")
        page += 1


def backfill_shards_from_raw() -> int:
    """One-shot: split an existing raw.parquet into per-customer shards so
    future resumable runs preserve already-ingested customers. Idempotent —
    if a customer's shard is already marked complete, it's left alone."""
    if not CT_MART["raw"].exists():
        log.info("No raw.parquet to backfill from.")
        return 0
    raw = pd.read_parquet(CT_MART["raw"])
    if raw.empty or "customer" not in raw.columns:
        log.warning("raw.parquet has no customer column — cannot backfill.")
        return 0
    SHARDS_DIR.mkdir(parents=True, exist_ok=True)
    n_backfilled = 0
    for customer in sorted(raw["customer"].dropna().unique()):
        existing = _load_shard_state(customer)
        if existing["complete"]:
            continue
        sub = raw[raw["customer"] == customer]
        if sub.empty:
            continue
        slug = _customer_slug(customer)
        shard_dir = SHARDS_DIR / slug
        shard_dir.mkdir(parents=True, exist_ok=True)
        sub.to_parquet(shard_dir / "page_0001.parquet", index=False)
        _save_shard_state(customer, {
            "last_completed_page": 1,
            "total_count": len(sub),
            "complete": True,
            "rows": len(sub),
            "backfilled_from_raw": True,
        })
        n_backfilled += 1
        log.info(f"  backfilled {customer}: {len(sub):,} rows")
    log.info(f"Backfilled {n_backfilled} customer(s) into shards.")
    return n_backfilled


def _merge_all_shards_to_raw() -> int:
    """Concat every customer's shard pages into a single raw.parquet.
    Returns total rows written."""
    if not SHARDS_DIR.exists():
        log.warning("No shards directory — nothing to merge")
        return 0

    parts: list[pd.DataFrame] = []
    total = 0
    for cust_dir in sorted(SHARDS_DIR.iterdir()):
        if not cust_dir.is_dir():
            continue
        pages = sorted(cust_dir.glob("page_*.parquet"))
        if not pages:
            continue
        for p in pages:
            df = pd.read_parquet(p)
            parts.append(df)
            total += len(df)

    if not parts:
        log.warning("Shards directory has no page parquets")
        return 0

    merged = pd.concat(parts, ignore_index=True)
    merged.to_parquet(CT_MART["raw"], index=False)
    log.info(f"raw.parquet written: {len(merged):,} rows ← merge of {len(parts)} shard pages")
    return len(merged)


def _fetch_customer(
    customer: str,
    division: str,
    begin_date: str | None,
) -> pd.DataFrame:
    """Legacy in-memory fetch — kept for backwards-compat with the live router.
    The pipeline run() path uses _fetch_customer_resumable instead."""
    log.info(f"  → {customer} ({division})")
    records = fetch_all_pages(customer, division, begin_date=begin_date)
    if not records:
        log.info(f"      no records returned")
        return pd.DataFrame()
    df = _normalise_page_df(records, customer, division)
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
    # When --only is given, we preserve the ORDER the user typed them in so
    # callers can deliberately run smallest → biggest (or any order they want).
    # --exclude doesn't reorder.
    by_name = {c["customer"].lower(): c for c in CT_CUSTOMERS}
    if only:
        seen = set()
        customers = []
        for name in only:
            cfg = by_name.get(name.lower())
            if cfg and cfg["customer"].lower() not in seen:
                customers.append(cfg)
                seen.add(cfg["customer"].lower())
        log.info(f"Filter --only:    {only}    → {len(customers)} customer(s) selected (in --only order)")
    else:
        exclude_set = {c.lower() for c in exclude} if exclude else None
        customers = [
            c for c in CT_CUSTOMERS
            if exclude_set is None or c["customer"].lower() not in exclude_set
        ]
        if exclude:
            log.info(f"Filter --exclude: {exclude} → {len(customers)} customer(s) remaining")

    SHARDS_DIR.mkdir(parents=True, exist_ok=True)
    failed: list[str] = []
    partial: list[str] = []
    complete: list[str] = []
    total = len(customers)
    is_full = (mode == "full")

    for i, cust in enumerate(customers, start=1):
        if progress_cb:
            try: progress_cb(cust["customer"], i - 1, total)
            except Exception: pass
        try:
            ok = _fetch_customer_resumable(
                customer  = cust["customer"],
                division  = cust["division"],
                begin_date= begin_date,
                full      = is_full,
            )
            (complete if ok else partial).append(cust["customer"])
        except Exception as e:
            log.error(f"  CRASHED {cust['customer']}: {e}")
            failed.append(cust["customer"])
        if progress_cb:
            try: progress_cb(None, i, total)
            except Exception: pass

    # Merge all shards (including any from prior runs not in this customer list)
    # into raw.parquet.
    total_rows = _merge_all_shards_to_raw()

    if total_rows == 0:
        log.warning("No data on disk after this run.")
        if failed:  log.error(f"Crashed customers:  {failed}")
        if partial: log.error(f"Partial customers:  {partial}")
        return False

    # Persist top-level state
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    state.update({
        "last_run_date":     now,
        "last_run_mode":     mode,
        "total_rows":        total_rows,
        "complete_customers": complete,
        "partial_customers":  partial,
        "failed_customers":   failed,
    })
    _save_state(state)

    log.info(f"Complete: {len(complete)} | Partial (resume next run): {len(partial)} | Crashed: {len(failed)}")
    if partial: log.warning(f"Partial customers will resume on next --incremental: {partial}")
    if failed:  log.error  (f"Crashed customers (need investigation): {failed}")
    log.info("CYCLE TIME INGEST  complete")
    return True
