import os
import sqlite3
import pandas as pd

DB  = os.path.join(os.path.dirname(__file__), "data", "option_chain.db")
OUT = os.path.join(os.path.expanduser("~"), "Desktop", "option_chain.csv")

conn = sqlite3.connect(DB)
tables = [
    "nifty50_option_chain",
    "banknifty_option_chain",
    "midcapnifty_option_chain",
    "finnifty_option_chain",
    "sensex_option_chain",
]

frames = []
for t in tables:
    df = pd.read_sql(f"SELECT * FROM {t}", conn)
    if not df.empty:
        df["source_table"] = t
        frames.append(df)
        print(f"{t}: {len(df)} rows")
    else:
        print(f"{t}: empty, skipping")

conn.close()

if frames:
    out = pd.concat(frames, ignore_index=True)
    out.to_csv(OUT, index=False, float_format="%.6g")
    print(f"\nExported {len(out)} rows -> {OUT}")
else:
    print("No data to export.")
