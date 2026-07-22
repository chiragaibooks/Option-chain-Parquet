import sqlite3

conn = sqlite3.connect("data/option_chain.db")
tables = [
    "nifty50_option_chain",
    "banknifty_option_chain",
    "finnifty_option_chain",
    "midcapnifty_option_chain",
    "sensex_option_chain",
]

print("=" * 70)
print(f"{'TABLE':<30} {'TS':>4} {'ROWS':>6} {'NULL_G':>7} {'NULL_IV':>8}")
print("=" * 70)

for t in tables:
    ts    = conn.execute(f"SELECT DISTINCT timestamp FROM {t} WHERE timestamp LIKE '20260721%' ORDER BY timestamp").fetchall()
    total = conn.execute(f"SELECT COUNT(*) FROM {t} WHERE timestamp LIKE '20260721%'").fetchone()[0]
    nullg = conn.execute(f"SELECT COUNT(*) FROM {t} WHERE timestamp LIKE '20260721%' AND delta IS NULL").fetchone()[0]
    nulliv= conn.execute(f"SELECT COUNT(*) FROM {t} WHERE timestamp LIKE '20260721%' AND iv IS NULL").fetchone()[0]
    first = ts[0][0]  if ts else "—"
    last  = ts[-1][0] if ts else "—"
    print(f"{t:<30} {len(ts):>4} {total:>6} {nullg:>7} {nulliv:>8}   {first} -> {last}")

print()
print("=== Greeks NULL breakdown by option_type (July 21) ===")
for t in tables:
    for ot in ("CE", "PE"):
        r = conn.execute(
            f"SELECT COUNT(*) FROM {t} WHERE timestamp LIKE '20260721%' AND option_type=? AND delta IS NULL",
            (ot,)
        ).fetchone()[0]
        tot = conn.execute(
            f"SELECT COUNT(*) FROM {t} WHERE timestamp LIKE '20260721%' AND option_type=?",
            (ot,)
        ).fetchone()[0]
        if tot > 0:
            pct = round(r / tot * 100, 1)
            print(f"  {t:<30} {ot}  NULL={r}/{tot} ({pct}%)")

print()
print("=== Sample NULL-greek rows (nifty50, July 21) ===")
rows = conn.execute(
    "SELECT timestamp, option_type, expiry, strike, spot, ltp, iv, delta "
    "FROM nifty50_option_chain WHERE timestamp LIKE '20260721%' AND delta IS NULL LIMIT 10"
).fetchall()
for r in rows:
    print(r)

conn.close()
