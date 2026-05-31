# Cycle Time → Workcell Reporting — Plan

> Separating **what we build first (simple)** from **where this is eventually going (the end game)**,
> so the small step makes sense without committing to the whole vision yet.
> Date: 2026-05-31

---

## 0. The realization

The IEDB pull gave us **far more than cycle time**. Every process row also carries:

| Column | Meaning | Fill rate | Useful for |
|---|---|---|---|
| `cycle_time_per_process` | how long the process takes | 100% | cycle time (what we show today) |
| `order` | process **sequence** in the routing | 100% | true process flow / build order |
| `hc` | **headcount** (operators) per process | 95% | labor content |
| `fpy` | **first-pass yield** | 100% | quality |
| `cap` | capacity | 100% | throughput / UPH |
| `mach` / `hand` | machine vs manual time split | 50–70% | work-content analysis |
| `updated_on` | when the standard was last set | 100% | data governance / freshness |
| `grp` | GRP standard group | 100% | linking to PPQT later |
| `pb` | **unknown — flagged, do not surface** | 70% | TBD (confirm with IE) |
| `lct`, `imt`, `quote` | mostly empty | 0–8% | ignore |

So a "workcell" (customer) is really a fully-profileable manufacturing entity.
Cycle time is the entry point, not the whole story.

---

## 1. The end game (the vision — NOT what we build now)

Eventually, each workcell becomes a drillable report across these layers:

```
Workcell (customer)
  └─ Line (sub_workcenter)
       └─ Assembly (part number + revision)
            └─ Process (ordered routing)
```

…and at each layer you can see the relevant dimension:

- **Cycle time** — how long to build (per process, per assembly, per line)
- **Routing** — the ordered process flow (using `order`)
- **Labor** — operators per build (`hc`)
- **Work content** — machine vs manual split (`mach`/`hand`)
- **Quality** — first-pass yield (`fpy`)
- **Bottleneck / line balance** — which process constrains the line
- **Freshness** — how current the standard is (`updated_on`)

End-game extras (much later, only noting them so the direction is clear):
- Cross-module joins — cycle-time **standard** vs OLE **actual** vs PPQT **target**
- Feed clean, structured tables to AI/analytics jobs
- A unified data tree (the bronze/silver/gold discussion — parked for now)

**This whole section is the destination, not the next commit.** It exists so the
small first step below is understood as step 1 of something coherent — not a one-off.

---

## 2. What we build FIRST (simple, temporary, additive)

**A Workcell Breakdown page** — one new layer on the Cycle Time module.

Goal: pick a workcell, see it **broken down by line and assembly**, showing the
**cycle-time facts** in an organized way. That's it. No contested "hero insight,"
no bottleneck framing decisions, no charts, no topology assumptions.

### Scope (what it shows)
- **Header**: workcell name + plain counts — assemblies, lines, processes, data freshness
- **By line** (sub_workcenter): each line with # assemblies and its cycle-time range/typical build time
- **By assembly**: list of assemblies (per line) with total build time + # processes
- Drill direction: Workcell → Line → Assembly (and the existing table already shows the per-process detail)

### Explicitly NOT in the first step
- ❌ Bottleneck hero / "MA 1 is the constraint" framing (needs topology input — parked)
- ❌ Machine-vs-manual charts, FPY dashboards, capacity (later layers)
- ❌ Any assumption about whether SUB/feeder lines combine into one build
- ❌ Touching the existing overview table (stays the main data reference)

### How it attaches
- The existing Cycle Time page gets a **tabbed view**: `Table` (default, unchanged) + `Breakdown` (new), sharing the same selected workcell.
- Backend: a single read-only endpoint (`/api/cycle-time/profile`) already drafted —
  returns counts + per-line summary + per-assembly list. We present it plainly.

---

## 3. Roadmap (how step 1 grows into the end game)

| Step | Layer added | Status |
|---|---|---|
| **1** | **Workcell breakdown page** (counts + by-line + by-assembly, cycle-time only) | ← build this now |
| 2 | Assembly **routing view** — ordered process flow (`order`) with per-step cycle time | next |
| 3 | **Labor** layer — headcount per build (`hc`) | later |
| 4 | **Bottleneck / line balance** (needs line-topology answer) | later |
| 5 | **Quality** (`fpy`) + **work content** (`mach`/`hand`) | later |
| 6 | Cross-module (OLE actual vs standard) + AI feeds | end game |

Each step is additive and shippable on its own. We stop and review after each.

---

## 4. Open items (parked, not blocking step 1)
- `pb` column meaning — unknown, flagged, not surfaced
- Line topology: are SUB/STOSA feeder lines into ENDO, or independent builds? (only matters from step 4)
- Bronze/silver/gold data-tree restructure (separate discussion)
