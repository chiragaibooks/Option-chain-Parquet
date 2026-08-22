"""
generate_parquet.py
Exports real option chain data from option_chain.db to parquet files.
One parquet file per trading day: data/option_chain_YYYYMMDD.parquet

Usage:
    python generate_parquet.py                        # all dates in DB
    python generate_parquet.py 20260819               # single date
    python generate_parquet.py 20260817 20260819      # date range
"""
import os
import sqlite3
import sys
from datetime import datetime

import pandas as pd

DB_PATH    = "data/option_chain.db"
OUTPUT_DIR = "data"


def export_date(date_prefix: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(
            "SELECT * FROM nifty50_option_chain WHERE substr(timestamp,1,8)=? ORDER BY timestamp",
            conn,
            params=(date_prefix,),
        )
    if df.empty:
        print(f"No data found for {date_prefix}")
        return
    path = os.path.join(OUTPUT_DIR, f"option_chain_{date_prefix}.parquet")
    df.to_parquet(path, index=False)
    print(f"Exported {date_prefix}: {df['timestamp'].nunique()} timestamps, {len(df):,} rows -> {path}")


def all_dates_in_db() -> list:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT DISTINCT substr(timestamp,1,8) FROM nifty50_option_chain ORDER BY 1"
        ).fetchall()
    return [r[0] for r in rows]


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    args = sys.argv[1:]

    if len(args) == 0:
        dates = all_dates_in_db()
        print(f"Exporting all {len(dates)} dates from DB...")
    elif len(args) == 1:
        dates = [args[0]]
    else:
        start = datetime.strptime(args[0], "%Y%m%d")
        end   = datetime.strptime(args[1], "%Y%m%d")
        with sqlite3.connect(DB_PATH) as conn:
            rows = conn.execute(
                "SELECT DISTINCT substr(timestamp,1,8) FROM nifty50_option_chain "
                "WHERE substr(timestamp,1,8) BETWEEN ? AND ? ORDER BY 1",
                (args[0], args[1]),
            ).fetchall()
        dates = [r[0] for r in rows]
        print(f"Exporting {len(dates)} dates from {args[0]} to {args[1]}...")

    for d in dates:
        export_date(d)


if __name__ == "__main__":
    main()
