from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR         = Path(__file__).parent
DATA_RAW_DIR     = BASE_DIR / "data" / "raw"
DATA_MART_DIR    = BASE_DIR / "data" / "mart"

# Network share where MES and eTMS CSVs are exported to
# Recent files land in NETWORK_PATH directly; older/archived files are in RawData/
NETWORK_PATH     = Path(r"\\penhomev10\OLE")
RAWDATA_PATH     = Path(r"\\penhomev10\OLE\RawData")

# ─── CSV filename patterns (date suffix: _YYYYMMDD) ───────────────────────────
PRODUCTION_PREFIX     = "PEN_TotalProduction_"
PAID_HOURS_RAW_PREFIX = "PEN_PaidHours_Raw_"         # row-level from RawData — USE THIS

# ─── SMH source files (stored in data/raw/) ───────────────────────────────────
# Comment on each line indicates which SMH stage column is used for that workcell.
# This is the authoritative source — do not auto-detect from data.
SMH_FILES = {
    "AOP1":                DATA_RAW_DIR / "AOP1_SMH.xls",           # SMT
    "ARISTA NETWORKS PCA": DATA_RAW_DIR / "ARISTA_SMH.xls",         # SMT  (renamed from "ARISTA NETWORKS")
    "ARISTA NETWORKS HLA": DATA_RAW_DIR / "ARISTA_HLA_SMH.xls",     # Backend
    "ASP":                 DATA_RAW_DIR / "ASP_SMH.xls",             # BoxBuild
    "LAM RESEARCH":        DATA_RAW_DIR / "LAM_SMH.xls",             # Backend
    "BECKMAN COULTER":     DATA_RAW_DIR / "BC_SMH.xls",              # SMT  (re-enabled)
    "IMED PCA":            DATA_RAW_DIR / "IMED_SMH.xls",            # SMT  (renamed from "IMED")
    "KEYSIGHT HLA":        DATA_RAW_DIR / "KEYSIGHT_HLA_SMH.xls",   # BoxBuild
    "UTAS":                DATA_RAW_DIR / "UTAS_SMH.xls",            # Backend
    "WABTEC":              DATA_RAW_DIR / "WABTEC_SMH.xls",          # Backend

    # --- SMH files available but workcell not yet active ---
    # "KEYSIGHT":          DATA_RAW_DIR / "KEYSIGHT_PCA_SMH.xls",   # PCA variant — pending

    # --- Workcells in CSV with no SMH file yet (cannot be activated) ---
    # "DYSON"      "INFINERA"  "IROBOT"   "K IXIA"   "LAM RESEARCH"
    # "MSI"        "MSI HLA"   "PHOTONICS" "TELLABS"  "TMO"
    # SUPPORT P1 / SUPPORT P2 / WAREHOUSE P1 / WAREHOUSE P2 — indirect labor, no SMH needed
}

# ─── Workcell config ──────────────────────────────────────────────────────────
# scan_stage : SubWorkcell value in MES that represents this workcell's final output scan
# smh_col    : which SMH column to use for the OLE numerator
# label      : human-readable stage label for the dashboard
# plant      : plant grouping for frontend filtering
#              "Plant 1" = main plant  |  "Plant 2" = Batu Kawan / ARISTA lines
WORKCELL_CONFIG = {
    "ASP": {
        "scan_stage": "BoxBuild",
        "smh_col":    "SMH/ Unit - BoxBuild",
        "label":      "BoxBuild",
        "plant":      "Plant 1",
    },
    "AOP1": {
        "scan_stage": "SMT",
        "smh_col":    "SMH/ Unit - SMT",
        "label":      "SMT",
        "plant":      "Plant 1",
    },
    "KEYSIGHT HLA": {
        "scan_stage": "BoxBuild",
        "smh_col":    "SMH/ Unit - BoxBuild",
        "label":      "BoxBuild",
        "plant":      "Plant 1",
    },
    "WABTEC": {
        "scan_stage": "Backend",
        "smh_col":    "SMH/ Unit - Backend",
        "label":      "Backend",
        "plant":      "Plant 1",
    },
    "UTAS": {
        "scan_stage": "Backend",
        "smh_col":    "SMH/ Unit - Backend",
        "label":      "Backend",
        "plant":      "Plant 1",
    },
    "BECKMAN COULTER": {
        "scan_stage": "SMT",
        "smh_col":    "SMH/ Unit - SMT",
        "label":      "SMT",
        "plant":      "Plant 1",
    },
    "IMED PCA": {
        "scan_stage": "SMT",
        "smh_col":    "SMH/ Unit - SMT",
        "label":      "SMT",
        "plant":      "Plant 1",
    },
    "ARISTA NETWORKS PCA": {
        "scan_stage": "SMT",
        "smh_col":    "SMH/ Unit - SMT",
        "label":      "SMT",
        "plant":      "Plant 2",
    },
    "ARISTA NETWORKS HLA": {
        "scan_stage": "Backend",
        "smh_col":    "SMH/ Unit - Backend",
        "label":      "Backend",
        "plant":      "Plant 2",
    },
    "LAM RESEARCH": {
        "scan_stage": "Backend",
        "smh_col":    "SMH/ Unit - Backend",
        "label":      "Backend",
        "plant":      "Plant 1",
    },
}

# ─── Indirect labor (non-workcell entities) ─────────────────────────────────
# Warehouses and support pools. Have paid hours but NO production / NO SMH.
# Not measured by OLE — tracked as overhead.
INDIRECT_LABOR_CONFIG = {
    "WAREHOUSE P1": {"label": "Warehouse P1", "plant": "Plant 1"},
    "WAREHOUSE P2": {"label": "Warehouse P2", "plant": "Plant 2"},
    "SUPPORT P1":   {"label": "Support P1",   "plant": "Plant 1"},
    "SUPPORT P2":   {"label": "Support P2",   "plant": "Plant 2"},
}

# All active workcell names — used to filter MES and eTMS data.
# Derived automatically from WORKCELL_CONFIG keys.
ACTIVE_WORKCELLS = list(WORKCELL_CONFIG.keys())

# Combined list of every entity ingest should keep (workcells + indirect labor).
ACTIVE_ENTITIES = list(WORKCELL_CONFIG.keys()) + list(INDIRECT_LABOR_CONFIG.keys())

# ─── Date range ───────────────────────────────────────────────────────────────
# Fixed historical start date for data ingestion.
DATE_FROM = "2025-01-01"

# ─── Mart filenames ───────────────────────────────────────────────────────────
MART = {
    "production":      DATA_MART_DIR / "raw_production.parquet",
    "paid_hours":      DATA_MART_DIR / "raw_paid_hours.parquet",
    "smh":             DATA_MART_DIR / "smh_lookup.parquet",
    "ole":             DATA_MART_DIR / "ole_computed.parquet",
    "smh_status":      DATA_MART_DIR / "smh_assembly_status.parquet",
    "ole_weekly":      DATA_MART_DIR / "ole_weekly.parquet",
    "indirect_labor":  DATA_MART_DIR / "indirect_labor.parquet",
}
