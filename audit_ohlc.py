import sqlite3

conn = sqlite3.connect("data/option_chain.db")

print("=== All July 20 timestamps (nifty50) ===")
r = conn.execute(
    "SELECT DISTINCT timestamp FROM nifty50_option_chain "
    "WHERE timestamp >= '202607200000' AND timestamp < '202607210000' ORDER BY timestamp"
).fetchall()
for x in r:
    print(x[0])

print()
print("=== OHLC for CE 24500 all days ===")
r2 = conn.execute(
    "SELECT timestamp, expiry, ltp, open, high, low, close "
    "FROM nifty50_option_chain WHERE strike=24500.0 AND option_type='CE' ORDER BY timestamp"
).fetchall()
for x in r2:
    print(x)

print()
print("=== OHLC bug check: rows where open != first_ltp of day ===")
r3 = conn.execute("""
    WITH first_ltp AS (
        SELECT option_type, expiry, strike,
               substr(timestamp,1,8) AS day,
               MIN(timestamp) AS first_ts
        FROM nifty50_option_chain
        GROUP BY option_type, expiry, strike, substr(timestamp,1,8)
    ),
    first_vals AS (
        SELECT t.option_type, t.expiry, t.strike, f.day, t.ltp AS first_ltp
        FROM nifty50_option_chain t
        JOIN first_ltp f
          ON t.option_type=f.option_type AND t.expiry=f.expiry
         AND t.strike=f.strike AND t.timestamp=f.first_ts
    )
    SELECT t.timestamp, t.option_type, t.expiry, t.strike,
           t.ltp, t.open, fv.first_ltp,
           CASE WHEN round(t.open,2) != round(fv.first_ltp,2) THEN 'MISMATCH' ELSE 'ok' END AS status
    FROM nifty50_option_chain t
    JOIN first_vals fv
      ON t.option_type=fv.option_type AND t.expiry=fv.expiry
     AND t.strike=fv.strike AND substr(t.timestamp,1,8)=fv.day
    WHERE round(t.open,2) != round(fv.first_ltp,2)
    LIMIT 20
""").fetchall()
if r3:
    print(f"Found {len(r3)} open!=first_ltp mismatches:")
    for x in r3:
        print(x)
else:
    print("No open mismatches found.")

print()
print("=== OHLC bug check: rows where high < ltp ===")
r4 = conn.execute(
    "SELECT timestamp, option_type, expiry, strike, ltp, high "
    "FROM nifty50_option_chain WHERE high < ltp LIMIT 10"
).fetchall()
if r4:
    for x in r4: print(x)
else:
    print("No high < ltp violations.")

print()
print("=== OHLC bug check: rows where low > ltp ===")
r5 = conn.execute(
    "SELECT timestamp, option_type, expiry, strike, ltp, low "
    "FROM nifty50_option_chain WHERE low > ltp LIMIT 10"
).fetchall()
if r5:
    for x in r5: print(x)
else:
    print("No low > ltp violations.")

print()
print("=== Gap analysis: consecutive timestamp diffs ===")
r6 = conn.execute(
    "SELECT DISTINCT timestamp FROM nifty50_option_chain ORDER BY timestamp"
).fetchall()
ts_list = [x[0] for x in r6]
from datetime import datetime
gaps = []
for i in range(1, len(ts_list)):
    t1 = datetime.strptime(ts_list[i-1], "%Y%m%d%H%M")
    t2 = datetime.strptime(ts_list[i],   "%Y%m%d%H%M")
    diff = (t2 - t1).total_seconds() / 60
    if diff > 5:
        gaps.append((ts_list[i-1], ts_list[i], diff))

if gaps:
    print(f"Found {len(gaps)} gaps > 5 min:")
    for g in gaps:
        print(f"  {g[0]} -> {g[1]}  ({g[2]:.0f} min gap)")
else:
    print("No gaps > 5 min found.")

conn.close()
