import sys
sys.path.insert(0, r'C:\Users\91984\Desktop\Indexes-TA\stock-data-cornjob')

import sqlite3
from src.database import _update_greeks, _OC_TABLES

DB = r'C:\Users\91984\Desktop\Indexes-TA\stock-data-cornjob\data\option_chain.db'
conn = sqlite3.connect(DB)

for symbol, table in _OC_TABLES.items():
    # find the last known good spot for each date with spot=0
    bad_dates = conn.execute(f"""
        SELECT DISTINCT substr(timestamp,1,8) FROM {table}
        WHERE spot = 0 OR spot IS NULL
    """).fetchall()

    for (d,) in bad_dates:
        # get last valid spot from any row in this table before or on this date
        row = conn.execute(f"""
            SELECT spot FROM {table}
            WHERE spot > 0
            ORDER BY timestamp DESC
            LIMIT 1
        """).fetchone()

        if not row:
            print(f"[{symbol}] {d} — no valid spot found, skipping")
            continue

        spot = row[0]
        updated = conn.execute(f"""
            UPDATE {table} SET spot = ?
            WHERE (spot = 0 OR spot IS NULL)
            AND substr(timestamp,1,8) = ?
        """, (spot, d)).rowcount
        print(f"[{symbol}] {d} — fixed spot to {spot} for {updated} rows")

    conn.commit()

    # now recompute Greeks for all NULL delta rows
    dates = conn.execute(f"""
        SELECT DISTINCT substr(timestamp,1,8) FROM {table}
        WHERE delta IS NULL
    """).fetchall()
    for (d,) in dates:
        _update_greeks(conn, table, d)
    conn.commit()

# final check
print("\n--- Final NULL delta counts ---")
for symbol, table in _OC_TABLES.items():
    r = conn.execute(f"SELECT COUNT(*) FROM {table} WHERE delta IS NULL").fetchone()
    print(f"[{symbol}] {r[0]} NULL delta rows remaining")

conn.close()
print("\nDone.")
