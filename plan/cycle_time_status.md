# Cycle Time — Status & Backlog

> Snapshot of what's built, what's running, and what's queued.
> Date: 2026-05-29

---

## 1. Current state

### Backend
- **OAuth client_credentials** auth to IEDB working (`modules/cycle_time/auth.py`) — token cache + 60s expiry buffer + thread lock
- **Resumable per-page ingest** — each page saved to disk immediately, `.state.json` tracks `last_completed_page`, retry-with-backoff (5s/15s/45s × 3) on timeouts
- **Pivot pipeline** — alias-on-pivot with fallback to process when alias is null (recovered DYSON + ADVA)
- **Endpoints live** at `/api/cycle-time/*`:
  - `GET  /health` · `GET  /customers` · `GET  /aliases` · `GET  /data` · `GET  /raw`
  - `GET  /live` · `POST /refresh` · `GET  /refresh/status`
  - `/data` and `/live` drop all-null columns server-side (821 → ~19 for ASP)

### Frontend (IE-Pulse, `app-switcher` branch)
- Standalone Cycle Time app at `/ietools/cycle-time`
- **DB ↔ Live** source toggle in header
- **Virtualized** table via `@tanstack/react-virtual`
- **Frozen left columns** (Assembly + Line)
- **Sortable** column headers (asc → desc → unsorted)
- **Process** in header, **Alias** in tooltip (multi-process aliases wrap to multiple lines)
- Seconds with 2dp in cells (`19800.21s`), `H H MM M SS s` in tooltip
- **XLSX download** with frozen header + autofilter
- Customer dropdown sorted alphabetically
- Filter bar matches OLE styling (no shading, OLE label/select pattern)
- Vertical column lines, compact row height, opaque sticky cells (no scroll bleed-through)

### Data on disk
- `data/mart/cycle_time/raw.parquet` — 294,927 rows × 26 customers
- `data/mart/cycle_time/pivoted.parquet` — 22,916 rows × 907 alias columns (union)
- `data/mart/cycle_time/raw_shards/` — per-customer page parquets + `.state.json` (26 shards marked complete)

---

## 2. Customers — ingest status

### Complete (26)
ASP · BECKMAN COULTER · DYSON · MICRON SIG · Motorola · TMO · FORTALEZA · Masimo · ARISTA_NETWORKS_GLACIER · WABTEC · Nokia Optics · BD · UTAS · ILLUMINA · INTEL OPTICS · ResMed · HMB · ELENION TECHNOLOGIES · LAMMEC · AKAMAI · ADVA · Medtronic · ENDURANCE · LAMGB · AMAT · GOPRO

### Empty / no cycle time data in IEDB (8) — diagnosed
Customer exists with assemblies but IE engineers haven't entered cycle times yet. Will populate automatically on future ingests once they're added.

BEDFORD · AFC · ADVANTEST · LIFE360 · TERRA SANA · BARCO · Skydio · GO

### Pending (7) — the big customers
| # | Customer | Assemblies | Est. duration |
|---|---|---:|---|
| 1 | LTX | 7,228 | ~10–15 min |
| 2 | K_CTEC | 9,101 | ~15–20 min |
| 3 | LAMRESEARCH | 9,502 | ~15–20 min |
| 4 | INFINERA | 9,926 | ~15–20 min |
| 5 | Tellabs | 13,618 | ~25–30 min |
| 6 | ARISTANETWORKS | 15,151 | ~30–40 min |
| 7 | KEYSIGHT | 59,539 | ~2–4 hours |

**Total expected wall time:** 4–6+ hours.

---

## 3. The command to run

After PC restart:

```cmd
cd "C:\Users\4033375\Projects\OLE ANALYZER\ole-backend" && venv\Scripts\activate && python -m modules.cycle_time.pipeline.refresh --full --only "LTX,K_CTEC,LAMRESEARCH,INFINERA,Tellabs,ARISTANETWORKS,KEYSIGHT"
```

### What it does
1. For each of the 7 customers, fetch page-by-page (PageSize=500)
2. Each page → immediate write to `data/mart/cycle_time/raw_shards/<customer>/page_NNNN.parquet`
3. Update `.state.json` after every successful page
4. On timeout: retry 3× with backoff; on full failure → customer marked partial, all completed pages remain on disk
5. At end of run, all shards (including the 26 existing) merge into `raw.parquet`, then transform rebuilds `pivoted.parquet`

### If it crashes / you have to stop / PC sleeps
Just re-run the same command. The resumable design:
- Skips already-complete customers
- Resumes partial customers from `last_completed_page + 1`
- Never re-fetches pages that are already on disk

### How to check progress mid-run (separate terminal)
```cmd
type "data\mart\cycle_time\raw_shards\KEYSIGHT\.state.json"
```
Look for `last_completed_page` advancing.

---

## 4. Backlog (after big-7 ingest finishes)

| # | Task | Effort | Priority |
|---|---|---|---|
| **B** | Standard process flow ordering — read sorted `cycle_time_processes.md` → reorder FE columns by physical sequence | ~45 min | High — biggest UX uplift |
| **C** | PPQT ingestion (`/api/grp-standard/ppqt`) — adds the **target** value per process; FE shows actual-vs-target color coding | ~1.5 hr | Medium |
| **D** | GRP Summary ingestion (`/api/Report/GetGRPSummaryReport`) — per-assembly KPIs (UPH, bottleneck, HC, SMH) | ~1 hr | Medium |
| F | Live mode `sub_workcenter` server-side filter — IF IEDB supports it, narrow KEYSIGHT-style queries to one line at a time | ~30 min probe + ~1 hr if supported | Low — DB mode covers this once KEYSIGHT is ingested |
| G | Schedule periodic incremental refresh (Windows Task) — daily/weekly auto-pull of updated records | ~30 min | Low — once data shape stabilises |

---

## 5. Git status

Backend (`master`):
```
1742bbe fix(cycle-time): preserve --only customer order
eefb1a2 fix(cycle-time): --full preserves partial shards
64e1a3e feat(cycle-time): resumable per-page ingest + retry-with-backoff
fc633bd fix(cycle-time): prune empty columns + alias→process fallback
f827889 feat: Cycle Time module + per-module project layout
```

Frontend (`app-switcher`):
```
813be0f feat(cycle-time): new standalone app for Cycle Time analytics
```

All committed. Nothing pending push.

---

## 6. Robustness notes (what's protected)

- **Page timeout / 5xx / connection error** → 3 retries with backoff before giving up the page
- **Customer crash** → other customers unaffected, run continues
- **Token expiry** → auto-refresh handles it
- **Ctrl+C / PC sleep / reboot** → resume from last completed page
- **Re-run --full** → preserves partial shards (never wipes in-flight data)
- **Disk write atomicity** → page written as `.tmp` then renamed; state updated AFTER page is durable
- **External raw.parquet corruption** → next run regenerates from shards

What's NOT protected: manual deletion of `raw_shards/`, mid-run config changes, IEDB schema changes mid-page.
