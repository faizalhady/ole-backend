"""
client.py
─────────
HTTP client for the IEDB3.0 API.

Auth: handled by modules.cycle_time.auth (OAuth client_credentials flow with
      in-process token cache). No manual token paste — set IEDB_CLIENT_KEY in
      .env and tokens refresh automatically.

Endpoint used:
  GET /api/rawdataapi/v3/GetDetailRawProcessData
  Returns one row per (assembly, revision, sub_workcenter, process) with cycleTimePerProcess.
"""

import logging
import time

import requests

from modules.cycle_time.auth   import get_token, invalidate as invalidate_token
from modules.cycle_time.config import API_TIMEOUT, BASE_URL, PAGE_SIZE, SITE_CODE

# Transient-error retry — how many times we retry a timed-out / 5xx page
# before giving up on it (per page, NOT per customer).
_MAX_RETRIES = 3
_BACKOFF_BASE_S = 5.0   # 5s, 15s, 45s exponential

log = logging.getLogger(__name__)

_ENDPOINT = f"{BASE_URL}/api/rawdataapi/v3/GetDetailRawProcessData"


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {get_token()}",
        "Accept":        "application/json",
    }


def fetch_page(
    customer: str,
    division: str,
    page: int,
    page_size: int = PAGE_SIZE,
    begin_date: str | None = None,
    end_date: str | None = None,
) -> list[dict]:
    """Fetch a single page of raw process data for one customer/division.

    Resilience:
      - 401: invalidates cached token + retries once
      - Timeout / 5xx: retries up to _MAX_RETRIES times with exponential backoff
      - 4xx (other than 401/403): bubbles up as HTTPError
      - 403: raises PermissionError immediately (auth-level, no retry helps)
    """
    params: dict = {
        "SiteCode":   SITE_CODE,
        "Customer":   customer,
        "PageNumber": page,
        "PageSize":   page_size,
    }
    if division:
        params["Division"] = division
    if begin_date:
        params["BeginDate"] = begin_date
    if end_date:
        params["EndDate"] = end_date

    last_exc: Exception | None = None
    for attempt in range(_MAX_RETRIES + 1):  # 1 try + N retries
        try:
            resp = requests.get(_ENDPOINT, headers=_headers(), params=params, timeout=API_TIMEOUT)

            if resp.status_code == 401:
                log.warning("401 from IEDB — invalidating cached token and retrying once")
                invalidate_token()
                resp = requests.get(_ENDPOINT, headers=_headers(), params=params, timeout=API_TIMEOUT)
                if resp.status_code == 401:
                    raise PermissionError(
                        "401 Unauthorized after token refresh — check IEDB_CLIENT_KEY in .env."
                    )
            if resp.status_code == 403:
                raise PermissionError(f"403 Forbidden for customer='{customer}'. Check your access rights.")

            if resp.status_code >= 500:
                # Transient — retry
                raise requests.HTTPError(f"{resp.status_code} {resp.reason}", response=resp)

            resp.raise_for_status()
            return resp.json() or []

        except (requests.Timeout, requests.HTTPError, requests.ConnectionError) as e:
            last_exc = e
            if attempt >= _MAX_RETRIES:
                break
            backoff = _BACKOFF_BASE_S * (3 ** attempt)  # 5s, 15s, 45s
            log.warning(
                f"  page {page} attempt {attempt + 1}/{_MAX_RETRIES + 1} failed ({type(e).__name__}: {e}) — "
                f"retrying in {backoff:.0f}s"
            )
            time.sleep(backoff)

    # All retries exhausted
    raise RuntimeError(f"Page {page} failed after {_MAX_RETRIES + 1} attempts: {last_exc}") from last_exc


def fetch_all_pages(
    customer: str,
    division: str,
    page_size: int = PAGE_SIZE,
    begin_date: str | None = None,
    end_date: str | None = None,
) -> list[dict]:
    """
    Paginate through all pages for a customer/division and return all records.
    Uses totalCount (present on every row) to know when to stop.
    Falls back to empty-page detection if totalCount is absent.
    """
    all_records: list[dict] = []
    page = 1

    while True:
        log.debug(f"    page {page} …")
        batch = fetch_page(customer, division, page, page_size, begin_date, end_date)

        if not batch:
            break

        all_records.extend(batch)

        # Use totalCount from first record if available
        total = batch[0].get("totalCount")
        if total is not None and len(all_records) >= total:
            break

        # Fallback: if page wasn't full, we're done
        if len(batch) < page_size:
            break

        page += 1

    return all_records
