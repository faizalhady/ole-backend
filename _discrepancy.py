from dotenv import load_dotenv; from pathlib import Path
load_dotenv(Path('.env'))
import pandas as pd
from modules.cycle_time.config import CT_CUSTOMERS, CT_MART
from modules.cycle_time.client import fetch_all_pages

EXCLUDE = {'KEYSIGHT', 'ARISTANETWORKS', 'ARISTA_NETWORKS_GLACIER'}
raw = pd.read_parquet(CT_MART['raw'], columns=['customer', 'assembly'])

def acol(df):
    for c in df.columns:
        if c.lower() == 'assembly': return c
    return None

rows = []
for c in CT_CUSTOMERS:
    name = c['customer']
    if name in EXCLUDE: continue
    ours = raw[raw['customer'] == name]
    our_rows, our_asm = len(ours), ours['assembly'].nunique()
    try:
        recs = fetch_all_pages(name, c['division'])
        df = pd.DataFrame(recs)
        ie_rows = len(df)
        ie_asm = df[acol(df)].nunique() if ie_rows and acol(df) else 0
        err = ''
    except Exception as e:
        ie_rows = ie_asm = -1; err = str(e)[:40]
    gap_asm = (ie_asm - our_asm) if ie_asm >= 0 else None
    rows.append((name, our_rows, ie_rows, our_asm, ie_asm, gap_asm, err))
    print(f"{name:28s} rows {our_rows:>7}/{ie_rows:<7} asm {our_asm:>4}/{ie_asm:<4} gap_asm {gap_asm} {err}", flush=True)

print("\n===== SUMMARY (customers with assembly gaps) =====")
flagged = [r for r in rows if r[5] and r[5] != 0]
flagged.sort(key=lambda r: -(r[5] or 0))
print(f"{'customer':28s} {'our_asm':>8} {'iedb_asm':>8} {'gap':>5}")
for r in flagged:
    print(f"{r[0]:28s} {r[3]:>8} {r[4]:>8} {r[5]:>+5}")
print(f"\ncustomers checked: {len(rows)} | with gaps: {len(flagged)} | total missing assemblies: {sum((r[5] or 0) for r in flagged)}")
