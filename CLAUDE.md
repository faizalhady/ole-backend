# IE Pulse — Backend CLAUDE.md
# C:\Users\4033375\Projects\OLE ANALYZER\ole-backend

## What This Is
This is the **IE Pulse backend** — a FastAPI monorepo serving all IE analytical modules
for Jabil Penang. The folder name "OLE ANALYZER" is legacy and irrelevant. The product
is called IE Pulse.

The paired frontend lives at:
  C:\Users\4033375\Projects\PRODUCTION DASHBOARD\IE-Pulse\

---

## Stack
- Python / FastAPI + uvicorn
- pandas + pyarrow — all computed data stored as parquet (the "mart")
- duckdb — used for analytical queries over parquet files
- openpyxl / beautifulsoup4 / lxml — Excel and HTML-disguised XLS parsing
- SQLite (core/database.py) — user-entered operational data only (downtime, transfers)
- statsmodels — OLE forecasting / prediction endpoint
- requests + python-dotenv — Cycle Time module external API client

---

## Repo Structure

```
ole-backend/
│
├── api/
│   ├── main.py              # FastAPI app entry point — registers all module routers
│   ├── deps.py              # Shared dependencies
│   └── routers/             # One file per module — all endpoints live here
│       ├── ole.py           ✅ live
│       ├── downtime.py      ✅ live
│       ├── transfers.py     ✅ live
│       ├── cycle_time.py    ✅ live
│       ├── ppqt.py          ✅ live
│       ├── lbr.py           ✅ live
│       └── ipk.py           🔲 stubbed — needs full implementation
│
├── core/                    # Shared across ALL modules — never add module-specific logic here
│   ├── database.py          # SQLite: downtime_logs, transfer_logs tables
│   ├── paths.py             # PROJECT_ROOT, DATA_RAW_DIR, DATA_MART_DIR
│   └── naming.py            # Shared naming helpers
│
├── modules/                 # One folder per module — all business logic lives here
│   ├── ole/                 ✅ live
│   │   ├── config.py        # Workcell config, network paths, mart paths, SMH files
│   │   └── pipeline/
│   │       ├── ingest.py    # Pull from \\penhomev10\OLE network share
│   │       ├── compute.py   # Daily OLE calculation
│   │       ├── compute_mh.py
│   │       ├── compute_weekly.py
│   │       └── refresh.py   # Pipeline entry point
│   │
│   ├── cycle_time/          ✅ live
│   │   ├── config.py
│   │   ├── auth.py          # External IEDB3.0 auth
│   │   ├── client.py        # HTTP client for CT data source
│   │   ├── keep_awake.py
│   │   └── pipeline/
│   │       ├── ingest.py
│   │       ├── transform.py
│   │       └── refresh.py
│   │
│   ├── lbr/                 ✅ live (pipeline stubbed, router live)
│   │   ├── config.py
│   │   └── pipeline/
│   │       └── refresh.py
│   │
│   ├── ppqt/                ✅ live
│   │   ├── config.py
│   │   └── pipeline/
│   │       └── refresh.py
│   │
│   └── ipk/                 🔲 STUB — this is what we're building next
│       ├── config.py        # Expand: add mart paths + workcell settings
│       └── pipeline/
│           └── refresh.py   # Placeholder only — rewrite
│
├── data/
│   ├── raw/                 # SMH XLS files, uploaded Excel inputs
│   ├── mart/
│   │   ├── ole/             # OLE computed parquets
│   │   ├── cycle_time/      # CT computed parquets
│   │   └── ipk/             # IPK parquets (to be created)
│   └── operational.db       # SQLite: downtime_logs, transfer_logs
│
└── scripts/
    ├── diagnose.py
    └── setup_scheduled_tasks.ps1
```

---

## Module Pattern (follow this for every module)

```
modules/<name>/
    config.py           ← mart dir + mart file paths + module constants
    pipeline/
        refresh.py      ← entry point, called by the router via BackgroundTasks
        ingest.py       ← pull/parse raw data from source
        compute.py      ← run calculations, produce dataframes
        export.py       ← write dataframes to parquet mart
```

```
api/routers/<name>.py
    prefix = /api/<name>
    GET  /health        ← always include, checks mart file existence
    POST /refresh       ← triggers pipeline as BackgroundTask
    GET  /data          ← serves mart data to frontend
```

Router calls `from modules.<name>.pipeline.refresh import run` — that's the only coupling.

---

## Modules — Status & Purpose

| Module     | Status     | Purpose |
|------------|------------|---------|
| ole        | ✅ Live     | Overall Line Efficiency — daily OLE % per workcell, SMH, man-hours |
| cycle_time | ✅ Live     | Cycle time data pulled from IEDB3.0 external system |
| ppqt       | ✅ Live     | Capacity analysis — takt time, resources needed per process |
| lbr        | ✅ Live     | Line Balance Rate — workload balance across stations |
| downtime   | ✅ Live     | Downtime log entry and reporting (SQLite) |
| transfers  | ✅ Live     | Cross-workcell man-hour transfer logs (SQLite) |
| ipk        | 🔲 Stub    | In-Process Kanban — WIP buffer calculation between processes |

---

## IPK Module — What It Is

IPK calculates the maximum WIP (boards) allowed between two adjacent production processes,
then converts that to a number of trolleys.

### Core Formula Chain
```
Effective UPH = (3600 / Bottleneck_CT_sec) × FPY × Efficiency × Conversion% × Qty_Machines

Conversion% = 1 - ((changeover_time_min / 60 × num_changeovers) / total_available_hours)

IPK_raw = (UPH_upstream - UPH_downstream) × (Loading_Qty / UPH_upstream)

IPK_clamped = MAX(IPK_raw, 0)          # negative = upstream slower = no buffer needed

WIP_Estimated = FLOOR(IPK_clamped × 1.15)    # 15% non-occupancy buffer

Trolleys_Needed = CEIL(WIP_Estimated / Boards_per_Trolley)   # always round UP
```

### Calculation Types
- `normal`          — standard formula above
- `double_pass`     — SMT bot + top; calculate both, take MAX (never sum)
- `multi_loop`      — repeated process; calculate each loop, take MAX
- `piece_to_batch`  — continuous process feeding a batch process
- `batch_to_piece`  — batch process feeding a continuous process
- `batch_to_batch`  — both sides are batch processes
- `two_line_input`  — two upstream lines feeding one downstream; combine UPH first

### Data Sources (all from Excel file uploads by IE engineer)
| File | Contents |
|------|----------|
| Cycle Time Matrix | Bottleneck CT per product × process group, FPY, efficiency, changeover time |
| Avail Machine Matrix | Qty equipment per product × process group |
| Trolley Type Matrix | Trolley type + boards per trolley per product |
| Process Grouping | Which stations belong to which IPK zone |
| Loading Plan | Weekly/monthly demand per product (from planner) |
| PPQT settings | Hours/shift, days/period |

### Files to Build
```
modules/ipk/
├── config.py              EXPAND  — add mart file paths + workcell settings
├── pipeline/
│   ├── refresh.py         REWRITE — orchestrate full pipeline
│   ├── ingest.py          NEW     — parse all Excel source files
│   ├── compute.py         NEW     — run IPK calculations for one demand period
│   └── export.py          NEW     — write results to parquet mart
└── engine/                NEW DIR — pure calculation functions, zero I/O
    ├── __init__.py
    ├── conversion.py      — conversion_pct per process group
    ├── uph.py             — effective_uph per product × group
    ├── ipk_normal.py      — standard IPK formula + clamping
    ├── ipk_double_pass.py — take MAX across passes
    ├── ipk_batch.py       — batch variants
    ├── ipk_two_lines.py   — merge 2 upstream lines
    ├── wip_buffer.py      — apply 15% non-occupancy buffer
    ├── trolley_converter.py — wip_estimated → trolleys_needed
    └── ipk_matrix.py      — demand-tier × trolley matrix builder

api/routers/ipk.py         REWRITE — replace placeholder with real endpoints
```

### IPK API Endpoints (all under /api/ipk)
```
GET  /health
POST /refresh                           ← background task (follows OLE pattern)
POST /upload                            ← accept Excel file uploads
POST /runs                              ← trigger a calculation run {workcell, period}
GET  /runs/{id}                         ← poll run status
GET  /runs/{id}/results                 ← full per-product × per-group table
GET  /runs/{id}/summary                 ← aggregated per process group
PUT  /runs/{id}/summary/{group_id}      ← manual inputs: in/out, reject, on-hold trolleys
GET  /workcells/{wc}/matrix             ← IPK Matrix vs Demand table
GET  /workcells/{wc}/history            ← all past runs
GET  /runs/{id}/export                  ← Excel/PDF download
```

### IPK Key Rules
- Negative IPK → clamp to 0
- Double pass / multi-loop → take MAX, never sum
- Trolleys → always CEIL
- WIP buffer → fixed 15% (non_occupancy_buffer)
- Period type → support both weekly and monthly

---

## Key Conventions

- All computed data → parquet mart (never SQLite)
- SQLite → user-entered operational data only (downtime_logs, transfer_logs)
- Router files are thin — logic lives in modules/, not routers/
- Background tasks via FastAPI BackgroundTasks (see ole_router.refresh pattern)
- No auth on endpoints currently — open API
- CORS is open (allow_origins=["*"])

---

## Architecture Docs (Notion)
https://www.notion.so/IPK-371fc83bd2fc8081aa67c99c5b6c04d3

---

## What To Work On Next
- [ ] Expand modules/ipk/config.py
- [ ] Create modules/ipk/engine/ — start with uph.py and ipk_normal.py
- [ ] Create modules/ipk/pipeline/ingest.py
- [ ] Create modules/ipk/pipeline/compute.py
- [ ] Rewrite api/routers/ipk.py with real endpoints
