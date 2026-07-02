"""
cleanup_inf.py — Replace any inf/-inf values in market_data.db with NULL.
Run once: python cleanup_inf.py
"""
import sqlite3
import math

DB = "data/market_data.db"

conn = sqlite3.connect(DB)

# Get all REAL columns from indexes table
real_cols = [
    row[1] for row in conn.execute("PRAGMA table_info(indexes)")
    if row[2].upper() == "REAL"
]
print(f"Checking {len(real_cols)} REAL columns...")

total_fixed = 0
for col in real_cols:
    # SQLite stores inf as a float — check using typeof and value
    result = conn.execute(f"""
        UPDATE indexes SET {col} = NULL
        WHERE typeof({col}) = 'real'
          AND ({col} = 9e999 OR {col} = -9e999)
    """)
    fixed = conn.execute("SELECT changes()").fetchone()[0]
    if fixed:
        print(f"  {col}: fixed {fixed} rows")
        total_fixed += fixed

conn.commit()
conn.close()
print(f"\nDone. Total rows fixed: {total_fixed}")
