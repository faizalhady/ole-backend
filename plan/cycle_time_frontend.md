# Cycle Time — Frontend Plan & Findings

> **Status:** Backend live (ASP ingested as Phase A dry-run). FE not started.
> **Date:** 2026-05-28
> **Author:** Solo
> **Companion doc:** [cycle_time_module.md](./cycle_time_module.md) (backend / data)

---

## 1. Backend state (recap — already done)

- OAuth `client_credentials` auth via `modules/cycle_time/auth.py` — token cache + 60s expiry buffer + thread lock (ported from `iedb_auth_service.cs`)
- Live API verified — `/api/Customers/all` and `/api/rawdataapi/v3/GetDetailRawProcessData` both 200
- **Phase A dry-run complete** for customer **ASP**:
  - 9,708 raw rows → `data/mart/cycle_time/raw.parquet`
  - 1,080 pivoted rows × 15 process columns → `data/mart/cycle_time/pivoted.parquet`
  - `GET /api/cycle-time/data?customer=ASP&assembly=00-27000` returns the exact Image 2 layout
- **Bug found + fixed in `transform.py`:** `grp` and `playbook` were in the pivot index. They vary per process, so the pivot didn't collapse rows. Removed → 9708 → 1080 rows. ✅

**Not yet done:** Phase B (full 41-customer pull). Deliberately deferred until the FE is wired so we can verify end-to-end before scaling.

---

## 2. API endpoint comparison (findings)

Three endpoints relevant to Cycle Time:

| Endpoint | Granularity | Fields | Purpose |
|---|---|---|---|
| **`GetDetailRawProcessData`** | per (assembly, rev, sub_wc, **process**) | 32 | Actual `CycleTimePerProcess`. **Source of truth for Image 2 pivot.** |
| **`grp-standard/ppqt`** | per (customer, sub_wc, **process**) — no assembly | 8 | Target/standard time per (line, process). Used for variance analysis. |
| **`Report/GetGRPSummaryReport`** | per (assembly, rev, sub_wc) — pre-rolled | 26 | Headline KPIs: `Cycle`, `VAT`, `UPH`, `HC`, `SMH`, `Bottleneck`. |

**Current scope:** `GetDetailRawProcessData` only. PPQT and GRP Summary deferred to Phase 2.

### Live API quirks discovered
- Fields come back **PascalCase** (`Assembly`, `CycleTimePerProcess`) — swagger said camelCase. The `_camel_to_snake` regex in `ingest.py` handles both, so no code change needed.
- `TotalCount` is present (initial probe was wrong).
- `API_TIMEOUT` bumped 30s → 90s (KEYSIGHT timed out at 30s).
- `GO`, `Skydio`, etc. return 0 rows — those small customers genuinely have no cycle time data.

---

## 3. Data model — the row identity question

The pivoted table is keyed on **(customer, division, family, assembly, revision, workcenter, workcenter_type, sub_workcenter)** — NOT just (assembly, process).

**Why sub_workcenter must be in the row identity:**
Same assembly can be built on multiple lines, and cycle times differ. Example for `00-27000-0-001F`:

| Line | `Assembly 1` cycle time |
|---|---|
| ASP HLA ENDO P1B-2 | 19,800 s |
| ASP HLA ENDO SUB P1B-2 | 450 s |
| ASP HLA STOSA P1B-2 | 450 s |

Same part, same process name, 44× difference. If we collapsed to `(assembly, process)` we'd lose this.

**Three concepts with overlapping names (clarified):**
- **Assembly (part number / model)** — the SKU, e.g. `00-27000-0-001F`
- **Sub-workcenter (line)** — the physical line, e.g. `ASP HLA ENDO P1B-2`
- **Process step** (`Assembly 1`, `Hi-Pot 1`, `FNI 1`, …) — one step in the build flow. "Assembly 1" is a process name, NOT a part number.

**Null cells** mean "this line doesn't run that process for this part" — not missing data.

---

## 4. Frontend — existing IEPulse patterns (what we mirror)

| Concern | Existing OLE pattern | Cycle Time uses |
|---|---|---|
| API base URL | `/ietools/ole/api/*` (Vite proxies → `localhost:8000` in dev) | `/ietools/cycle-time/api/*` |
| API client | `src/lib/ole/oleApi.ts` — typed fetch wrapper | `src/lib/cycle_time/cycleTimeApi.ts` |
| Data hooks | `src/hooks/ole/useOleData.ts` — hand-rolled module-level `Map` cache, 5min TTL | `src/hooks/cycle_time/useCycleTimeData.ts` — **switching to React Query** |
| Pages | `src/pages/ole/<Page>.tsx` | `src/pages/cycletime/<Page>.tsx` (folder exists, empty) |
| App registry | `src/config/apps.ts` — each module is an `AppConfig` | Add `cycle_time` to `AppId` + push new entry |
| Build mode | `package.json` → `build:ole`, `build:pulse`, … | Add `build:cycletime` |
| Stack | Vite + React 18 + TS + shadcn/ui + Tailwind + Recharts | Same |

---

## 5. Final FE design decisions

| Decision | Choice | Rationale |
|---|---|---|
| Fetch strategy | **Per-customer on demand** | User picks customer → fetch only that customer's rows. Caches forever within session. Matches the natural data axis. Avoids 30MB upfront payload. |
| Process columns | **Dynamic from current data** | Each customer has its own process set (ASP: 15, KEYSIGHT: likely 20+). Show only what exists. Matches Image 2. |
| App placement | **New standalone app** | Own basename `/ietools/cycle-time`, own build mode, own AppSwitcher entry. Matches OLE's release/deploy independence. |
| Theme | **Match OLE exactly** | Same shadcn tokens, same Tailwind config. Apps should feel like one product. |
| Caching layer | **TanStack React Query** | Already in `package.json` but unused. Stale-while-revalidate, refetch on focus, devtools, mutation invalidation — all free. |

---

## 6. CT-specific enhancements (deltas vs OLE)

### A. New patterns we need that OLE doesn't have

| # | Enhancement | Why CT needs it | Backport to OLE? |
|---|---|---|---|
| 1 | `@tanstack/react-virtual` row virtualization | 150k+ pivoted rows after full ingest — DOM-rendering all of them freezes the browser | No — OLE row counts are small |
| 2 | Frozen left columns + horizontal scroll | 8 metadata + 15+ process columns = wider than viewport | No — OLE tables are narrow |
| 3 | Seconds → human-readable cell format (`5h 30m`) | `19800.21` is unreadable as a number | No — OLE deals in % and hours, already formatted |

### B. Improvements we'll add to CT that OLE could benefit from later

| # | Enhancement | Notes |
|---|---|---|
| 4 | **TanStack React Query** instead of hand-rolled Map cache | Try in CT first, evaluate for OLE migration after one sprint |
| 5 | **URL-driven filter state** via `useSearchParams` | Deep-linkable, refresh-safe, bookmarkable views |
| 6 | **Loading skeletons** (not just spinners) | Feels faster, shows incoming layout |
| 7 | **CSV / Excel export** (`exceljs` already in deps) | Engineers will want to paste cycle times into Excel |

### C. Backend-FE coordination specific to CT

| # | Enhancement | Notes |
|---|---|---|
| 8 | `GET /api/cycle-time/refresh/status` endpoint | `/refresh` is async (BackgroundTasks). Without status, FE can't show progress. Returns `{state, started_at, customers_done, customers_total, last_error}`. FE polls while running. |
| 9 | Auto-invalidate cached queries when refresh completes | FE detects status flip running→idle → invalidates React Query cache |

### D. Intentionally NOT changing

- App registry pattern in `apps.ts`
- Vite multi-mode build setup
- File layout (`lib/<module>/`, `hooks/<module>/`, `pages/<module>/`)
- shadcn theme tokens

---

## 7. File layout (FE)

```
IE-Pulse/
└── src/
    ├── lib/cycle_time/
    │   └── cycleTimeApi.ts             ← fetch wrapper + TS types for 6 endpoints
    │
    ├── hooks/cycle_time/
    │   └── useCycleTimeData.ts         ← React Query hooks: useCycleTimeHealth,
    │                                     useCycleTimeCustomers, useCycleTimeData,
    │                                     useCycleTimeRaw, useCycleTimeRefresh,
    │                                     useCycleTimeRefreshStatus
    │
    ├── pages/cycletime/
    │   ├── CycleTimeHome.tsx           ← landing — KPI cards + filter bar + table
    │   ├── CycleTimeTable.tsx          ← virtualized pivoted table (Image 2 layout)
    │   └── CycleTimeFilters.tsx        ← customer / line / search inputs
    │
    └── config/apps.ts                  ← +1 AppConfig entry, extend AppId union
```

**Page sketch (CycleTimeHome):**
```
┌──────────────────────────────────────────────────────────────────┐
│ Cycle Time                            [Refresh] [Status: idle]  │
├──────────────────────────────────────────────────────────────────┤
│ KPI cards: Total Assemblies | Lines | Processes | Last Updated  │
├──────────────────────────────────────────────────────────────────┤
│ Filters:  Customer ▼   Line ▼   Search assembly… [_______]      │
├──────────────────────────────────────────────────────────────────┤
│ [Virtualized table — CycleTimeTable component]                  │
│   Frozen: assembly, revision, sub_workcenter                    │
│   Scrollable: 15+ process columns                               │
└──────────────────────────────────────────────────────────────────┘
```

---

## 8. Execution order

| # | Step | Est. | Status |
|---|---|---|---|
| 1 | Backend: add `GET /api/cycle-time/refresh/status` | 10 min | ⬜ |
| 2 | FE: `cycleTimeApi.ts` typed client (6 endpoints) | 15 min | ⬜ |
| 3 | FE: `useCycleTimeData.ts` — React Query hooks per-customer | 25 min | ⬜ |
| 4 | FE: `apps.ts` registry entry + `vite.config.ts` proxy + `package.json` script | 10 min | ⬜ |
| 5 | FE: `CycleTimeFilters.tsx` + `CycleTimeTable.tsx` (virtualized) | 45 min | ⬜ |
| 6 | FE: `CycleTimeHome.tsx` — page shell | 20 min | ⬜ |
| 7 | Smoke test: `npm run dev` against backend serving ASP | 15 min | ⬜ |
| 8 | **Phase B trigger:** full 41-customer ingest once FE confirms correctness | ~1–2 hr | ⬜ |

---

## 9. Out of scope (Phase 2)

- PPQT ingestion → variance heatmap (actual vs target)
- GRP Summary ingestion → headline KPI strip
- Per-assembly drawer/detail view
- Incremental refresh mode (only meaningful after baseline full pull)
- Playwright-based token auto-refresh (current OAuth client_credentials flow is sufficient)
- OLE backport of React Query / URL filters / skeletons (evaluate after CT lives for one sprint)
