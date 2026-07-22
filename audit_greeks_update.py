import sqlite3

conn = sqlite3.connect("data/option_chain.db")

print("=== Schema of nifty50_option_chain ===")
cols = conn.execute("PRAGMA table_info(nifty50_option_chain)").fetchall()
for c in cols:
    print(f"  {c[1]:15s}  {c[2]}")

print()
print("=== Greeks updating across timestamps (CE 24000, 21-Jul-2026) ===")
rows = conn.execute("""
    SELECT timestamp, ltp, iv, delta, gamma, theta, vega, rho, open, high, low, close
    FROM nifty50_option_chain
    WHERE strike=24000.0 AND option_type='CE' AND expiry='21-Jul-2026'
    ORDER BY timestamp
""").fetchall()
print(f"{'timestamp':<15} {'ltp':>7} {'iv':>7} {'delta':>7} {'gamma':>9} {'theta':>8} {'vega':>7} {'rho':>7} {'open':>7} {'high':>7} {'low':>7} {'close':>7}")
for r in rows:
    print(f"{r[0]:<15} {str(r[1]):>7} {str(r[2]):>7} {str(r[3]):>7} {str(r[4]):>9} {str(r[5]):>8} {str(r[6]):>7} {str(r[7]):>7} {str(r[8]):>7} {str(r[9]):>7} {str(r[10]):>7} {str(r[11]):>7}")

print()
print("=== Are greeks changing across timestamps? (should differ as ltp/iv changes) ===")
rows2 = conn.execute("""
    SELECT COUNT(DISTINCT delta) as uniq_delta,
           COUNT(DISTINCT iv)    as uniq_iv,
           COUNT(DISTINCT ltp)   as uniq_ltp,
           COUNT(*)              as total
    FROM nifty50_option_chain
    WHERE strike=24000.0 AND option_type='CE' AND expiry='21-Jul-2026'
""").fetchone()
print(f"  total={rows2[3]}  unique_ltp={rows2[2]}  unique_iv={rows2[1]}  unique_delta={rows2[0]}")

print()
print("=== INSERT OR IGNORE check: are new timestamps being blocked? ===")
# Check if same (timestamp, option_type, expiry, strike) PK exists multiple times
dups = conn.execute("""
    SELECT timestamp, option_type, expiry, strike, COUNT(*) as cnt
    FROM nifty50_option_chain
    WHERE timestamp LIKE '20260721%'
    GROUP BY timestamp, option_type, expiry, strike
    HAVING cnt > 1
    LIMIT 5
""").fetchall()
print(f"  Duplicate PKs: {len(dups)} (should be 0)")

print()
print("=== _update_greeks: does it UPDATE existing rows or only NULL rows? ===")
# Check if a row with delta already set would get re-updated
# The WHERE clause is: delta IS NULL — so existing greeks are NEVER refreshed
print("  _update_greeks WHERE clause: delta IS NULL")
print("  => Greeks are computed ONCE at insert time and never refreshed")
print("  => If ltp/iv changes at next snapshot, greeks stay from first insert")
print("  => This is CORRECT for INSERT OR IGNORE pattern (each timestamp is a new PK)")

conn.close()
