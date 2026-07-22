"""
backfill_july21.py — one-off script to backfill NULL Greeks for July 21.
Run from project root: python backfill_july21.py
"""
import logging
import sys
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stdout)

from src.database import backfill_greeks_for_date

DB = "data/option_chain.db"

for date_str in ["20260721", "20260720"]:
    print(f"\n--- Backfilling {date_str} ---")
    backfill_greeks_for_date(DB, date_str)

print("\nDone.")
