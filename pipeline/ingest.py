"""
ingest.py
─────────
Loads raw data from four sources, normalises column names and values,
and writes clean Parquet files to the mart.

Sources
  1. MES production CSVs      → \\penhomev10\OLE\PEN_TotalProduction_*.csv
  2. eTMS paid hours raw       → \\penhomev10\OLE\RawData\PEN_PaidHours_Raw_*.csv
     (row-level; one row per employee; has TPHDirect only)
  3. eTMS paid hours agg       → \\penhomev10\OLE\PEN_TotalPaidHours_*.csv
     (aggregated per workcell/date/shift; has TPHSupport — required for OLE denominator)
  4. SMH XLS files             → data/raw/<WORKCELL>_SMH.xls  (HTML-disguised)

OLE denominator = TPHDirect + TPHSupport  (must match existing OLE web tool)
Raw paid hours file provides TPHDirect + VA/NVA employee detail.
Aggregated paid hours file provides TPHSupport (not in raw file).

Outputs  (data/mart/)
  raw_production.parquet
  raw_paid_hours.parquet
  raw_support_hours.parquet   ← NEW: TPHSupport per workcell/date/shift
  smh_lookup.parquet
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import re
import logging
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup

from config import (
    NETWORK_PATH,
    RAWDATA_PATH,
    DATA_MART_DIR,
    SMH_FILES,
    WORKCELL_CONFIG,
    ACTIVE_WORKCELLS,
    DATE_FROM,
    MART,
    PRODUCTION_PREFIX,
    PAID_HOURS_PREFIX,
    PAID_HOURS_RAW_PREFIX,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
log = logging.getLogger(__name__)

DATA_MART_DIR.mkdir(parents=True, exist_ok=True)


# --- Helpers ------------------------------------------------------------------

_WORKCELL_MAP: dict[str, str] = {
    "ASP":                  "ASP",
    "AOP1":                 "AOP1",
    "AOP 1":                "AOP1",
    "KEYSIGHT HLA":         "KEYSIGHT HLA",
    "KEYSIGHTHLA":          "KEYSIGHT HLA",
    "KEYSIGHT-HLA":         "KEYSIGHT HLA",
    "Keysight HLA":         "KEYSIGHT HLA",
    "WABTEC":               "WABTEC",
    "Wabtec":               "WABTEC",
    "UTAS":                 "UTAS",
    "Beckman Coulter":      "BECKMAN COULTER",
    "BECKMAN COULTER":      "BECKMAN COULTER",
    "IMED PCA":             "IMED",
    "IMED":                 "IMED",
    "Arista PCA":           "ARISTA NETWORKS",
    "ARISTA PCA":           "ARISTA NETWORKS",
    "ARISTA NETWORKS":      "ARISTA NETWORKS",
    "ARISTA":               "ARISTA NETWORKS HLA",
    "ARISTA NETWORKS HLA":  "ARISTA NETWORKS HLA",
}


def _normalise_workcell(name: str) -> str | None:
    if not isinstance(name, str):
        return None
    cleaned = name.strip()
    return _WORKCELL_MAP.get(cleaned) or _WORKCELL_MAP.get(cleaned.upper())


def _parse_date(value) -> pd.Timestamp | None:
    try:
        return pd.Timestamp(value)
    except Exception:
        return pd.NaT


def _cutoff_date() -> pd.Timestamp:
    return pd.Timestamp(DATE_FROM)


def _find_csv_files(prefix: str, search_dirs: list[Path]) -> list[Path]:
    """Scan given directories for CSVs matching prefix, filtered by DATE_FROM."""
    pattern = f"{prefix}*.csv"
    cutoff  = datetime.strptime(DATE_FROM, "%Y-%m-%d")
    files   = []
    seen    = set()
    date_re = re.compile(r"(\d{8})\.csv$")

    for search_dir in search_dirs:
        try:
            all_files = list(search_dir.glob(pattern))
        except Exception as e:
            log.warning(f"Cannot access {search_dir}: {e}")
            continue

        for f in sorted(all_files):
            if f.name in seen:
                continue
            seen.add(f.name)
            m = date_re.search(f.name)
            if m:
                try:
                    if datetime.strptime(m.group(1), "%Y%m%d") >= cutoff:
                        files.append(f)
                except ValueError:
                    files.append(f)
            else:
                files.append(f)

    log.info(f"Found {len(files)} file(s) for prefix '{prefix}'")
    return sorted(files)


# --- 1. MES Production --------------------------------------------------------

def ingest_production() -> pd.DataFrame:
    """Load and normalise MES production CSVs from both network paths."""
    files = _find_csv_files(PRODUCTION_PREFIX, [NETWORK_PATH, RAWDATA_PATH])
    if not files:
        log.warning("No production CSV files found.")
        return pd.DataFrame()

    frames = []
    for f in files:
        try:
            df = pd.read_csv(f, dtype=str)
            frames.append(df)
            log.info(f"  Loaded production: {f.name}  ({len(df)} rows)")
        except Exception as e:
            log.error(f"  Failed to read {f.name}: {e}")

    if not frames:
        return pd.DataFrame()

    df = pd.concat(frames, ignore_index=True)
    df.columns = [c.strip() for c in df.columns]

    df = df.rename(columns={
        "Site":           "site",
        "Workcell":       "workcell_raw",
        "SubWorkcell":    "sub_workcell",
        "AssemblyNumber": "assembly",
        "Qty":            "qty",
        "StartDate":      "date",
        "EndDate":        "end_date",
        "Shift":          "shift",
    })

    df["qty"]      = pd.to_numeric(df["qty"],   errors="coerce").fillna(0).astype(int)
    df["shift"]    = pd.to_numeric(df["shift"], errors="coerce").fillna(0).astype(int)
    df["date"]     = df["date"].apply(_parse_date)
    df["assembly"] = df["assembly"].str.strip().str.rstrip("/")
    df["workcell"] = df["workcell_raw"].apply(_normalise_workcell)

    unrecognised = df[df["workcell"].isna()]["workcell_raw"].dropna().unique()
    if len(unrecognised):
        log.info(f"  Production - unrecognised workcells (filtered out): {sorted(unrecognised)}")

    df = df[df["workcell"].notna()].copy()

    def _stage_match(row):
        cfg = WORKCELL_CONFIG.get(row["workcell"], {})
        return str(row["sub_workcell"]).strip().upper() == cfg.get("scan_stage", "").upper()

    df = df[df.apply(_stage_match, axis=1)].copy()
    df = df[df["date"] >= _cutoff_date()].copy()
    df = df.drop_duplicates(subset=["workcell", "assembly", "date", "shift"], keep="last")
    df = df[["site", "workcell", "sub_workcell", "assembly", "qty", "date", "shift"]].copy()

    log.info(f"Production: {len(df)} rows after normalisation and filtering")
    return df


# --- 2. eTMS Paid Hours (Raw, employee-level) ----------------------------------

def ingest_paid_hours() -> pd.DataFrame:
    """
    Load row-level paid hours from PEN_PaidHours_Raw_*.csv in RawData only.
    Each row = one employee x one shift.

    Columns captured from raw file:
      Site, CostCenter, WorkCell, SubWorkCell,
      THCDirect, TPHDirect,
      Startdate, EndDate, Shift,
      Value1  (VA | NVA | blank -- labour category),
      Position, CV, Name, DateJoined, DayJoined, Category

    Note: THCSupport / TPHSupport do NOT exist in the raw file.
          Support hours are ingested separately from the aggregated file.
    """
    files = _find_csv_files(PAID_HOURS_RAW_PREFIX, [RAWDATA_PATH])
    if not files:
        log.warning("No raw paid hours CSV files found in RawData -- mart will be empty.")
        return pd.DataFrame()

    frames = []
    cutoff = _cutoff_date()
    active = set(_WORKCELL_MAP.keys())

    for f in files:
        try:
            try:
                df = pd.read_csv(f, dtype=str, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(f, dtype=str, encoding='windows-1252')

            wc_col   = next((c for c in df.columns if c.strip() == 'WorkCell'), None)
            date_col = next((c for c in df.columns if c.strip() == 'Startdate'), None)
            if wc_col:
                df = df[df[wc_col].isin(active)]
            if date_col:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                df = df[df[date_col] >= cutoff]

            if df.empty:
                log.info(f"  Skipped (no relevant rows): {f.name}")
                continue

            frames.append(df)
            log.info(f"  Loaded raw paid hours: {f.name}  ({len(df)} rows after early filter)")
        except Exception as e:
            log.error(f"  Failed to read {f.name}: {e}")

    if not frames:
        return pd.DataFrame()

    df = pd.concat(frames, ignore_index=True)
    df.columns = [c.strip() for c in df.columns]

    df = df.rename(columns={
        "Site":        "site",
        "CostCenter":  "cost_center",
        "WorkCell":    "workcell_raw",
        "SubWorkCell": "sub_workcell",
        "THCDirect":   "thc_direct",
        "TPHDirect":   "tph_direct",
        "Startdate":   "date",
        "EndDate":     "end_date",
        "Shift":       "shift",
        "Value1":      "value_type",
        "Position":    "position",
        "CV":          "cv",
        "Name":        "name",
        "DateJoined":  "date_joined",
        "DayJoined":   "day_joined",
        "Category":    "category",
    })

    df = df.drop(columns=["Custom01"], errors="ignore")

    df["thc_direct"]  = pd.to_numeric(df["thc_direct"], errors="coerce").fillna(0).astype(int)
    df["tph_direct"]  = pd.to_numeric(df["tph_direct"], errors="coerce").fillna(0.0)
    df["shift"]       = pd.to_numeric(df["shift"],      errors="coerce").fillna(0).astype(int)
    df["date"]        = df["date"].apply(_parse_date)
    df["value_type"]  = df["value_type"].fillna("").str.strip().str.upper()
    df["total_input_hours"] = df["tph_direct"]   # support hours added at compute stage

    df["workcell"] = df["workcell_raw"].apply(_normalise_workcell)

    unrecognised = df[df["workcell"].isna()]["workcell_raw"].dropna().unique()
    if len(unrecognised):
        log.info(f"  Raw paid hours - unrecognised workcells (filtered out): {sorted(unrecognised)}")

    df = df[df["workcell"].notna()].copy()
    df = df[df["date"] >= _cutoff_date()].copy()

    df = df.drop_duplicates(
        subset=["workcell", "name", "date", "shift", "value_type"],
        keep="last"
    )

    df = df[[
        "site", "cost_center", "workcell", "sub_workcell",
        "thc_direct", "tph_direct", "total_input_hours",
        "date", "shift",
        "value_type",
        "position", "cv", "name",
        "date_joined", "day_joined", "category",
    ]].copy()

    log.info(f"Raw paid hours: {len(df)} rows after normalisation and filtering")
    log.info(f"  value_type breakdown: {df['value_type'].value_counts().to_dict()}")
    return df


# --- 3. eTMS Support Hours (Aggregated) ---------------------------------------

def ingest_support_hours() -> pd.DataFrame:
    """
    Load TPHSupport from the aggregated PEN_TotalPaidHours_*.csv files.

    These files are pre-aggregated per workcell/subworkcell/date/shift and
    contain THCSupport + TPHSupport columns not present in the raw file.

    This data is used ONLY to add support hours to the OLE denominator:
      Total Input Hours = TPHDirect (from raw) + TPHSupport (from here)

    Output columns: workcell, date, shift, thc_support, tph_support
    """
    files = _find_csv_files(PAID_HOURS_PREFIX, [NETWORK_PATH, RAWDATA_PATH])
    if not files:
        log.warning("No aggregated paid hours CSV files found -- support hours will be zero.")
        return pd.DataFrame()

    frames = []
    cutoff = _cutoff_date()
    active = set(_WORKCELL_MAP.keys())

    for f in files:
        try:
            try:
                df = pd.read_csv(f, dtype=str, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(f, dtype=str, encoding='windows-1252')

            wc_col   = next((c for c in df.columns if c.strip() == 'WorkCell'), None)
            date_col = next((c for c in df.columns if c.strip() in ('Startdate', 'StartDate')), None)
            if wc_col:
                df = df[df[wc_col].isin(active)]
            if date_col:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                df = df[df[date_col] >= cutoff]

            if df.empty:
                log.info(f"  Skipped (no relevant rows): {f.name}")
                continue

            frames.append(df)
            log.info(f"  Loaded aggregated paid hours: {f.name}  ({len(df)} rows after early filter)")
        except Exception as e:
            log.error(f"  Failed to read {f.name}: {e}")

    if not frames:
        return pd.DataFrame()

    df = pd.concat(frames, ignore_index=True)
    df.columns = [c.strip() for c in df.columns]

    # Normalise date column name (file uses 'Startdate' or 'StartDate')
    if "Startdate" in df.columns and "date" not in df.columns:
        df = df.rename(columns={"Startdate": "date"})
    elif "StartDate" in df.columns and "date" not in df.columns:
        df = df.rename(columns={"StartDate": "date"})

    df = df.rename(columns={
        "WorkCell":    "workcell_raw",
        "SubWorkCell": "sub_workcell",
        "THCSupport":  "thc_support",
        "TPHSupport":  "tph_support",
        "Shift":       "shift",
    })

    # Validate required columns exist
    required = {"workcell_raw", "date", "shift", "tph_support"}
    missing  = required - set(df.columns)
    if missing:
        log.error(f"Aggregated paid hours file missing columns: {missing}. Support hours skipped.")
        return pd.DataFrame()

    df["tph_support"] = pd.to_numeric(df["tph_support"], errors="coerce").fillna(0.0)
    df["thc_support"] = pd.to_numeric(df.get("thc_support", 0), errors="coerce").fillna(0.0)
    df["shift"]       = pd.to_numeric(df["shift"], errors="coerce").fillna(0).astype(int)
    df["date"]        = df["date"].apply(_parse_date)

    df["workcell"] = df["workcell_raw"].apply(_normalise_workcell)
    df = df[df["workcell"].notna()].copy()
    df = df[df["date"] >= _cutoff_date()].copy()

    # Aggregate to workcell/date/shift level (sum across sub-workcells)
    df = (
        df.groupby(["workcell", "date", "shift"], as_index=False)
        .agg(thc_support=("thc_support", "sum"), tph_support=("tph_support", "sum"))
    )

    log.info(f"Support hours: {len(df)} rows (workcell/date/shift level)")
    log.info(f"  Total TPHSupport: {df['tph_support'].sum():,.2f} hrs")
    return df[["workcell", "date", "shift", "thc_support", "tph_support"]]


# --- 4. SMH Lookup ------------------------------------------------------------

_SMH_COL_INDEX = {
    "SMH/ Unit - SMT":      3,
    "SMH/ Unit - Backend":  4,
    "SMH/ Unit - BoxBuild": 5,
}


def _parse_smh_xls(path: Path, workcell: str) -> pd.DataFrame:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()
    except Exception as e:
        log.error(f"Cannot read SMH file {path}: {e}")
        return pd.DataFrame()

    soup    = BeautifulSoup(html, "lxml")
    cfg     = WORKCELL_CONFIG[workcell]
    col_idx = _SMH_COL_INDEX[cfg["smh_col"]]

    data = []
    for row in soup.find_all("tr"):
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if len(cols) < 6:
            continue
        try:
            smh_val = float(cols[col_idx]) if cols[col_idx] else 0.0
        except ValueError:
            smh_val = 0.0

        last_updated = pd.NaT
        if len(cols) >= 10:
            try:
                last_updated = pd.Timestamp(cols[9])
            except Exception:
                pass

        data.append({
            "assembly":     cols[1].strip().rstrip("/"),
            "smh_value":    smh_val,
            "last_updated": last_updated,
        })

    if not data:
        log.warning(f"No data rows found in {path.name}")
        return pd.DataFrame()

    df = pd.DataFrame(data)
    df["workcell"]    = workcell
    df["scan_stage"]  = cfg["scan_stage"]
    df["stage_label"] = cfg["label"]
    df["plant"]       = cfg["plant"]
    df = df[df["assembly"].str.len() > 0].copy()

    nonzero = (df["smh_value"] > 0).sum()
    log.info(
        f"  SMH {workcell} ({cfg['label']}): {len(df)} assemblies, "
        f"{nonzero} non-zero, {len(df) - nonzero} zero/missing"
    )
    return df[["workcell", "assembly", "smh_value", "scan_stage", "stage_label", "plant", "last_updated"]]


def ingest_smh() -> pd.DataFrame:
    frames = []
    for workcell, path in SMH_FILES.items():
        if workcell not in WORKCELL_CONFIG:
            continue
        if not path.exists():
            log.warning(f"SMH file NOT FOUND for {workcell}: {path}")
            continue
        df = _parse_smh_xls(path, workcell)
        if not df.empty:
            frames.append(df)

    if not frames:
        log.error("No SMH data loaded.")
        return pd.DataFrame()

    df = pd.concat(frames, ignore_index=True)
    df = df.drop_duplicates(subset=["workcell", "assembly"])
    log.info(f"SMH lookup: {len(df)} total assembly entries across {df['workcell'].nunique()} workcells")
    return df


# --- Entry point --------------------------------------------------------------

def run():
    log.info("=" * 60)
    log.info("INGEST  starting")
    log.info("=" * 60)

    prod    = ingest_production()
    hours   = ingest_paid_hours()
    support = ingest_support_hours()
    smh     = ingest_smh()

    if prod.empty:
        log.error("Production data is empty -- aborting ingest.")
        return False
    if hours.empty:
        log.error("Paid hours data is empty -- aborting ingest.")
        return False
    if smh.empty:
        log.error("SMH data is empty -- aborting ingest.")
        return False

    prod.to_parquet(MART["production"],     index=False)
    hours.to_parquet(MART["paid_hours"],    index=False)
    smh.to_parquet(MART["smh"],             index=False)

    if not support.empty:
        support.to_parquet(MART["support_hours"], index=False)
        log.info(f"  raw_support_hours.parquet -> {len(support)} rows")
    else:
        log.warning("Support hours empty -- raw_support_hours.parquet NOT written. OLE denominator will be direct-only.")

    log.info("Mart written:")
    log.info(f"  raw_production.parquet  -> {len(prod)} rows")
    log.info(f"  raw_paid_hours.parquet  -> {len(hours)} rows")
    log.info(f"  smh_lookup.parquet      -> {len(smh)} rows")
    log.info("INGEST  complete")
    return True


if __name__ == "__main__":
    run()
