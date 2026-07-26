"""
main.py — Market data pipeline orchestrator.
Run from project root: python -m src.main
"""
import json
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

load_dotenv()

MARKET_DB    = os.getenv("MARKET_DB",    "data/market_data.db")
LOG_DIR      = os.getenv("LOG_DIR",      "data/logs")
SYMBOLS_FILE = os.getenv("SYMBOLS_FILE", "config/symbols.json")
README_FILE  = os.getenv("README_FILE",  "README.md")

os.makedirs(LOG_DIR, exist_ok=True)
_fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
_fh  = RotatingFileHandler(os.path.join(LOG_DIR, "app.log"), maxBytes=5*1024*1024, backupCount=5)
_fh.setFormatter(_fmt)
_ch  = logging.StreamHandler(sys.stdout)
_ch.setFormatter(_fmt)
logging.basicConfig(level=logging.INFO, handlers=[_fh, _ch])
logger = logging.getLogger(__name__)

import pytz
from datetime import datetime as _dt
from src.database           import init_db, insert_data
from src.tradingview_client import get_tv
from src.fetch_data         import fetch_all
from src.readme_generator   import update_readme

_IST = pytz.timezone("Asia/Kolkata")


def _load_symbols():
    with open(SYMBOLS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    indexes = data.get("Indexes", [])
    if not indexes:
        raise ValueError("'Indexes' list is empty in symbols.json")
    return indexes


def _needs_fetch(db: str, symbols: list) -> bool:
    import sqlite3
    import datetime
    cutoff = (_dt.now(_IST) - datetime.timedelta(minutes=4)).strftime("%Y%m%d%H%M")
    try:
        with sqlite3.connect(db) as conn:
            row = conn.execute(
                "SELECT datetime FROM indexes WHERE stock_name=? AND datetime >= ? LIMIT 1",
                (symbols[0], cutoff)
            ).fetchone()
        return row is None
    except Exception:
        return True


def main() -> None:
    logger.info("=== market-data pipeline starting ===")

    index_cfgs = _load_symbols()
    init_db(MARKET_DB)

    symbol_labels = [c["label"] for c in index_cfgs]
    if _needs_fetch(MARKET_DB, symbol_labels):
        tv   = get_tv()
        data = fetch_all(tv, index_cfgs)
        for cfg in index_cfgs:
            label = cfg["label"]
            df    = data.get(label)
            if df is not None and not df.empty:
                try:
                    insert_data(MARKET_DB, label, df)
                except Exception:
                    logger.exception("[%s] insert_data failed", label)
    else:
        logger.info("Market data already fresh — skipping fetch")

    update_readme(README_FILE, MARKET_DB, symbol_labels)
    logger.info("=== Cycle complete ===")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Fatal error")
        sys.exit(1)
