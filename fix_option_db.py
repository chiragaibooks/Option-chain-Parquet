"""
fix_option_db.py
Deletes all rows where iv=18 AND delta IS NULL (old hardcoded-IV data).
Run once: python fix_option_db.py
"""
import sqlite3, os

DB = "data/option_chain.db"
TABLES = [
    "nifty50_option_chain",
    "banknifty_option_chain",
    "midcapnifty_option_chain",
    "finnifty_option_chain",
    "sensex_option_chain",
]

conn = sqlite3.connect(DB)
for t in TABLES:
    before = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    conn.execute(f"DELETE FROM {t} WHERE iv=18.0 AND delta IS NULL")
    after = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"{t}: deleted {before - after} bad rows, {after} remaining")

conn.commit()
conn.execute("VACUUM")
conn.commit()
conn.close()
print("Done. Run 'python -m src.main' to re-fetch with correct IV and Greeks.")
