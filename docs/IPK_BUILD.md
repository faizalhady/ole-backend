# IPK — In-Process Kanban (Backend)

> IE Pulse · Jabil Penang
> This document is BACKEND-FOCUSED. For frontend pages, mock data, hooks, and UI specs see `IE-Pulse/docs/IPK_BUILD.md`.

---

## 1. Module Context

### 1.1 What This Module Is

**In-Process Kanban (IPK)** is a calculation tool that determines the maximum amount of WIP (Work-In-Progress, measured in boards) allowed between two adjacent production processes, then converts that WIP limit into a physical number of trolleys.

**Business problem it solves:** Production lines are not perfectly balanced. Without a controlled WIP cap, the faster upstream process floods the slower downstream process — causing undetected quality defects, floor congestion, and reactive line management.

**Who uses it:** IE Engineers (Industrial Engineers).
**When:** Weekly or monthly, triggered by a new demand plan from the Planner.
**Output used for:** Trolley placement, procurement justification, layout approval.

### 1.2 How IPK Fits Into IE Pulse Backend

| Aspect | Detail |
|---|---|
| Module pattern | Follows `modules/<module>/pipeline/` pattern established by OLE |
| Router registration | Already registered in `api/main.py` (placeholder mounted) |
| Dependencies | None at runtime — currently self-contained. Future: pull PPQT settings + Cycle Time CT data |
| Storage | Parquet mart in `data/mart/ipk/` — same as OLE pattern |
| SQLite | Not used — no user-entered operational data in this module |

**Data dependencies (when fully built):**

- **PPQT** → IPK consumes FPY, efficiency, hours/shift, days/period, changeover time
- **Cycle Time** → IPK consumes bottleneck CT per process group per product
- For Phase 1, all data comes from IE-uploaded Excel files

### 1.3 All Variables (BE perspective)

#### Configuration Inputs (per workcell)

| Variable | Type | Source | Description |
|---|---|---|---|
| `days_per_period` | float | PPQT / Settings | Working days in the demand period |
| `hours_per_shift` | float | PPQT / Settings | Available hours per shift |
| `num_shifts` | int | PPQT / Settings | Shifts per day |
| `non_occupancy_buffer` | float | Settings | Default 0.15 (15%) |
| `period_type` | enum | Settings | `weekly` or `monthly` |

#### Changeover Inputs (per process group)

| Variable | Type | Source | Description |
|---|---|---|---|
| `changeover_time_min` | float | PPQT | Minutes lost per changeover |
| `num_changeovers` | int | Computed | Count of products with demand > 0 and valid CT |
| `conversion_pct` | float | Computed | `1 - (changeover_hours / total_available_hours)` |

#### Product Master Data

| Variable | Type | Source | Description |
|---|---|---|---|
| `assembly_pn` | str | CT Matrix | Unique product part number |
| `bottleneck_ct_sec` | float | CT Matrix | Slowest station CT (seconds) |
| `qty_equipment` | int | Avail Machine Matrix | Number of machines |
| `fpy` | float | CT Matrix / PPQT | First Pass Yield |
| `efficiency` | float | CT Matrix / PPQT | Line efficiency |
| `boards_per_trolley` | int | Trolley Matrix | Trolley capacity |

#### Demand Inputs

| Variable | Type | Source | Description |
|---|---|---|---|
| `loading_qty` | int | Loading Plan | Units to produce in the period |
| `period` | str | Loading Plan | Period identifier |

#### Computed Outputs (per product × process group)

| Variable | Formula |
|---|---|
| `effective_uph` | `(3600 / bottleneck_ct_sec) × fpy × efficiency × conversion_pct × qty_equipment` |
| `ipk_raw` | `(uph_upstream - uph_downstream) × (loading_qty / uph_upstream)` |
| `ipk_clamped` | `MAX(ipk_raw, 0)` |
| `wip_estimated` | `FLOOR(ipk_clamped × 1.15)` |
| `trolleys_needed` | `CEIL(wip_estimated / boards_per_trolley)` |

### 1.4 Calculation Types

| Type | Rule |
|---|---|
| `normal` | Standard formula |
| `double_pass` | Calculate per pass, take MAX (never sum) |
| `multi_loop` | Same process repeated — take MAX |
| `piece_to_batch` | Batch size drives calculation |
| `batch_to_piece` | Batch size drives calculation |
| `batch_to_batch` | Both batch — use batch sizes |
| `two_line_input` | Combine upstream UPH first |

### 1.5 Hard Rules (do not break)

- Negative IPK → clamp to 0
- Double pass / multi-loop → take MAX, never sum
- Trolleys → always CEIL
- WIP buffer → always 15% (`non_occupancy_buffer`)
- Computed data → parquet mart (never SQLite)

### 1.6 Current Status

| Component | Status | File |
|---|---|---|
| Router | ⬜ Stubbed | `api/routers/ipk.py` — placeholder endpoints (health, refresh, data) |
| Pipeline | ⬜ Stubbed | `modules/ipk/pipeline/refresh.py` — does nothing |
| Engine | ⬜ Not built | `modules/ipk/engine/` does not exist |
| Config | ⬜ Partial | `modules/ipk/config.py` — minimal mart paths only |
| Mart data | ⬜ Not generated | No parquet files exist yet |

---

## 2. Backend Build Spec

### 2.1 Files to Create/Modify

```
modules/ipk/
├── config.py                  EXPAND  (exists, add workcell settings + mart paths)
├── pipeline/
│   ├── refresh.py             REWRITE (replace placeholder — orchestrate full pipeline)
│   ├── ingest.py              NEW     (parse uploaded Excel source files)
│   ├── compute.py             NEW     (run IPK calculations for one demand period)
│   └── export.py              NEW     (write results to parquet mart)
└── engine/                    NEW DIR (pure calculation functions — zero I/O)
    ├── __init__.py
    ├── conversion.py          NEW     (conversion_pct per process group)
    ├── uph.py                 NEW     (effective_uph per product × group)
    ├── ipk_normal.py          NEW     (standard IPK formula + clamping)
    ├── ipk_double_pass.py     NEW     (take MAX across passes)
    ├── ipk_batch.py           NEW     (piece↔batch, batch↔batch variants)
    ├── ipk_two_lines.py       NEW     (merge 2 upstream lines)
    ├── wip_buffer.py          NEW     (apply 15% non-occupancy buffer)
    ├── trolley_converter.py   NEW     (wip_estimated → trolleys_needed)
    └── ipk_matrix.py          NEW     (demand-tier × trolley matrix builder)

api/routers/ipk.py             REWRITE (replace placeholder with real endpoints)
```

### 2.2 All Formulas (Python)

```python
# modules/ipk/engine/conversion.py
def calc_conversion_pct(days, hours_shift, num_shifts, changeover_min, num_changeovers):
    total_hours = days * hours_shift * num_shifts
    changeover_hours = (changeover_min / 60) * num_changeovers
    return 1 - (changeover_hours / total_hours)

# modules/ipk/engine/uph.py
def calc_effective_uph(bottleneck_ct_sec, fpy, efficiency, conversion_pct, qty_equipment):
    if bottleneck_ct_sec <= 0:
        return 0.0
    raw_uph = 3600 / bottleneck_ct_sec
    return raw_uph * fpy * efficiency * conversion_pct * qty_equipment

# modules/ipk/engine/ipk_normal.py
def calc_ipk(uph_upstream, uph_downstream, loading_qty):
    if uph_upstream <= 0:
        return 0.0
    ipk_raw = (uph_upstream - uph_downstream) * (loading_qty / uph_upstream)
    return max(ipk_raw, 0.0)    # clamp negative to zero

# modules/ipk/engine/ipk_double_pass.py
def calc_ipk_double_pass(ipk_pass1, ipk_pass2):
    return max(ipk_pass1, ipk_pass2)    # NEVER sum — always MAX

# modules/ipk/engine/wip_buffer.py
def apply_buffer(ipk_clamped, buffer_pct=0.15):
    import math
    return math.floor(ipk_clamped * (1 + buffer_pct))

# modules/ipk/engine/trolley_converter.py
def calc_trolleys(wip_estimated, boards_per_trolley):
    import math
    if boards_per_trolley <= 0:
        return 0
    return math.ceil(wip_estimated / boards_per_trolley)
```

### 2.3 API Endpoints (api/routers/ipk.py)

All endpoints under `/api/ipk/`.

```
GET  /api/ipk/health
POST /api/ipk/refresh                           ← trigger pipeline (BackgroundTask)
POST /api/ipk/upload                            ← accept Excel file uploads
POST /api/ipk/runs                              ← trigger calculation {workcell, period}
GET  /api/ipk/runs/{id}                         ← poll run status
GET  /api/ipk/runs/{id}/results                 ← full per-product × per-group table
GET  /api/ipk/runs/{id}/summary                 ← aggregated per process group
PUT  /api/ipk/runs/{id}/summary/{group_id}      ← save manual trolley inputs
GET  /api/ipk/workcells/{wc}/matrix             ← IPK Matrix vs Demand
GET  /api/ipk/workcells/{wc}/history            ← all past runs
GET  /api/ipk/runs/{id}/export                  ← Excel/PDF download
```

### 2.4 Data Mart Schema (parquet columns)

**ipk_results.parquet** — one row per product × process group × run

```
run_id              str
workcell            str
period              str
period_type         str         weekly | monthly
product_id          str
assembly_pn         str
process_group       str
calc_type           str
loading_qty         int
bottleneck_ct_sec   float
fpy                 float
efficiency          float
conversion_pct      float
qty_equipment       int
effective_uph       float
uph_upstream        float
uph_downstream      float
ipk_raw             float
ipk_clamped         float
wip_estimated       int
boards_per_trolley  int
trolleys_needed     int
eligible            bool
run_date            datetime
```

**ipk_summary.parquet** — one row per process group × run

```
run_id                  str
workcell                str
period                  str
process_group           str
total_ipk_units         int
total_trolleys_ipk      int
in_out_trolleys         int
reject_trolleys         int
on_hold_trolleys        int
total_trolleys_required int
actual_on_floor         int
variance                int
run_date                datetime
```

**ipk_matrix.parquet** — one row per workcell × demand tier × process group

```
workcell        str
process_group   str
demand_tier     int
trolleys        int
generated_date  datetime
```

### 2.5 Module Config (modules/ipk/config.py)

```python
from pathlib import Path
from core.paths import DATA_MART_DIR, DATA_RAW_DIR

IPK_RAW_DIR  = DATA_RAW_DIR  / "ipk"
IPK_MART_DIR = DATA_MART_DIR / "ipk"
IPK_RAW_DIR.mkdir(parents=True, exist_ok=True)
IPK_MART_DIR.mkdir(parents=True, exist_ok=True)

IPK_MART = {
    "results": IPK_MART_DIR / "ipk_results.parquet",
    "summary": IPK_MART_DIR / "ipk_summary.parquet",
    "matrix":  IPK_MART_DIR / "ipk_matrix.parquet",
}

# Default operating constants
NON_OCCUPANCY_BUFFER = 0.15        # 15% buffer applied to all IPK
DEFAULT_FPY          = 0.99        # Default if not provided
DEFAULT_EFFICIENCY   = 0.85        # Default if not provided

# Status thresholds (keep in sync with FE ipkConstants.ts)
VARIANCE_CRITICAL = 5
VARIANCE_WARNING  = 0
```

### 2.6 Pipeline Flow

```
1. POST /api/ipk/upload                    ← user uploads Excel files
   └→ saved to data/raw/ipk/<workcell>/<period>/
2. POST /api/ipk/runs {workcell, period}
   └→ BackgroundTask triggers run_ipk_pipeline()
       ├→ ingest.py        parse 5 Excel sheets → DataFrames
       ├→ compute.py       run calculations using engine/ functions
       └→ export.py        write 3 parquet files to data/mart/ipk/
3. GET /api/ipk/runs/{id}/results          ← read from parquet
4. GET /api/ipk/runs/{id}/summary          ← read from parquet
```

### 2.7 Backend Build Order

```
1. Expand modules/ipk/config.py
2. Create modules/ipk/engine/__init__.py
3. Create modules/ipk/engine/conversion.py
4. Create modules/ipk/engine/uph.py
5. Create modules/ipk/engine/ipk_normal.py
6. Create modules/ipk/engine/ipk_double_pass.py
7. Create modules/ipk/engine/ipk_batch.py
8. Create modules/ipk/engine/ipk_two_lines.py
9. Create modules/ipk/engine/wip_buffer.py
10. Create modules/ipk/engine/trolley_converter.py
11. Create modules/ipk/engine/ipk_matrix.py
12. Create modules/ipk/pipeline/ingest.py
13. Create modules/ipk/pipeline/compute.py
14. Create modules/ipk/pipeline/export.py
15. Rewrite modules/ipk/pipeline/refresh.py
16. Rewrite api/routers/ipk.py with real endpoints
```

### 2.8 Module vs Other Modules

| Aspect | OLE | Cycle Time | IPK |
|---|---|---|---|
| Data source | Network CSV | IEDB3.0 API | IE Excel uploads |
| Auth | None | Okta Bearer | None |
| Storage | Parquet | Parquet | Parquet |
| Engine subfolder | No | No | Yes (calculation-heavy) |
| API prefix | `/api/ole/` | `/api/cycle-time/` | `/api/ipk/` |
