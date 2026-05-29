"""
scripts/generate_process_alias_doc.py
─────────────────────────────────────
After the Cycle Time full ingest completes, run this to dump every distinct
(customer, sub_workcenter, process, alias) combination from raw.parquet into
a markdown file. The user uses this to define the standard process-flow order
per line.

  python -m scripts.generate_process_alias_doc

Writes:  plan/cycle_time_processes.md
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd

from core.paths import PROJECT_ROOT
from modules.cycle_time.config import CT_MART

OUT = PROJECT_ROOT / "plan" / "cycle_time_processes.md"


def main() -> int:
    raw_path = CT_MART["raw"]
    if not raw_path.exists():
        print(f"ERROR: {raw_path} not found. Run the ingest first.", file=sys.stderr)
        return 1

    df = pd.read_parquet(raw_path)
    print(f"Loaded {len(df):,} raw rows")

    # Keep only the columns we care about. Some may have NaN in alias when IEDB
    # didn't populate it — we surface those explicitly so user can decide.
    cols = ["customer", "sub_workcenter", "process", "alias"]
    df = df[cols].copy()
    df["alias"] = df["alias"].fillna("(no alias)")

    distinct = df.drop_duplicates().sort_values(cols).reset_index(drop=True)
    print(f"Distinct (customer, line, process, alias) combos: {len(distinct):,}")

    # ── Build markdown ──
    lines: list[str] = []
    lines.append("# Cycle Time — Process & Alias Catalog")
    lines.append("")
    lines.append("> Auto-generated from `data/mart/cycle_time/raw.parquet`.")
    lines.append("> Use this to define the **standard process flow** per (customer × line).")
    lines.append("> Same `process` code can map to different `alias` values across lines —")
    lines.append("> that's expected (the alias is the customer-facing name per line).")
    lines.append("")
    lines.append(f"**Total raw rows:** {len(df):,}")
    lines.append(f"**Distinct (customer, line, process, alias):** {len(distinct):,}")
    lines.append(f"**Customers covered:** {df['customer'].nunique()}")
    lines.append(f"**Production lines covered:** {df['sub_workcenter'].nunique()}")
    lines.append(f"**Distinct processes:** {df['process'].nunique()}")
    lines.append(f"**Distinct aliases:** {df['alias'].nunique()}")
    lines.append("")

    # ── Global summary tables ──
    lines.append("## 1. All distinct processes (system-wide)")
    lines.append("")
    proc_counts = df.groupby("process").size().sort_values(ascending=False)
    lines.append("| Process | # rows |")
    lines.append("|---|---:|")
    for proc, n in proc_counts.items():
        lines.append(f"| `{proc}` | {n:,} |")
    lines.append("")

    lines.append("## 2. All distinct aliases (system-wide)")
    lines.append("")
    alias_counts = df.groupby("alias").size().sort_values(ascending=False)
    lines.append("| Alias | # rows |")
    lines.append("|---|---:|")
    for alias, n in alias_counts.items():
        lines.append(f"| `{alias}` | {n:,} |")
    lines.append("")

    # ── Per-customer breakdown ──
    lines.append("## 3. Per-customer × per-line process flow")
    lines.append("")
    lines.append("Each table = one production line. Rows show every distinct")
    lines.append("`(process, alias)` pair observed on that line, ordered alphabetically.")
    lines.append("Re-order the rows to set the **standard flow** (top → bottom = step 1 → step N).")
    lines.append("")

    for customer in sorted(df["customer"].unique()):
        cust_rows = df[df["customer"] == customer]
        lines.append(f"### {customer}")
        lines.append("")
        for line in sorted(cust_rows["sub_workcenter"].unique()):
            sub = cust_rows[cust_rows["sub_workcenter"] == line]
            combos = sub[["process", "alias"]].drop_duplicates().sort_values(["process", "alias"])
            lines.append(f"#### `{line}`  —  {len(combos)} steps")
            lines.append("")
            lines.append("| # | Process | Alias |")
            lines.append("|---:|---|---|")
            for i, (_, row) in enumerate(combos.iterrows(), start=1):
                lines.append(f"| {i} | `{row['process']}` | `{row['alias']}` |")
            lines.append("")
        lines.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
