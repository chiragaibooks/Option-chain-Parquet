import sqlite3

conn = sqlite3.connect("data/option_chain.db")

# Find the exact contract from the screenshot (CE, close~189.95 at 11:37)
print("=== Finding the contract ===")
rows = conn.execute("""
    SELECT timestamp, option_type, expiry, strike, ltp, open, high, low, close, iv, delta
    FROM nifty50_option_chain
    WHERE timestamp LIKE '20260721%'
      AND ltp BETWEEN 168 AND 192
      AND open = 189.95
    ORDER BY strike, option_type, timestamp
    LIMIT 20
""").fetchall()
for r in rows:
    print(r)

print()
print("=== OHLC: how many rows have open=high=low=close (stuck) ===")
stuck = conn.execute("""
    SELECT COUNT(*) FROM nifty50_option_chain
    WHERE timestamp LIKE '20260721%'
      AND open = high AND high = low
      AND open IS NOT NULL
""").fetchone()[0]
total = conn.execute("SELECT COUNT(*) FROM nifty50_option_chain WHERE timestamp LIKE '20260721%'").fetchone()[0]
print(f"Stuck OHLC: {stuck}/{total} rows ({round(stuck/total*100,1)}%)")

print()
print("=== Greeks NULL count per timestamp (July 21) ===")
rows2 = conn.execute("""
    SELECT timestamp,
           COUNT(*) as total,
           SUM(CASE WHEN delta IS NULL THEN 1 ELSE 0 END) as null_g,
           SUM(CASE WHEN iv IS NULL THEN 1 ELSE 0 END) as null_iv
    FROM nifty50_option_chain
    WHERE timestamp LIKE '20260721%'
    GROUP BY timestamp
    ORDER BY timestamp
""").fetchall()
for r in rows2:
    print(r)

print()
print("=== Sample NULL-greek rows with ltp > 0 and iv present ===")
rows3 = conn.execute("""
    SELECT timestamp, option_type, expiry, strike, spot, ltp, iv, delta
    FROM nifty50_option_chain
    WHERE timestamp LIKE '20260721%'
      AND delta IS NULL
      AND ltp > 0
    LIMIT 15
""").fetchall()
for r in rows3:
    print(r)

conn.close()
