"""database.py — Parquet-only storage for option chain snapshots.

Each trading day gets its own file: data/option_chain_YYYYMMDD.parquet
No SQLite is used.
"""
import os
import logging
from datetime import datetime

import pandas as pd
import pytz

logger = logging.getLogger(__name__)
IST = pytz.timezone("Asia/Kolkata")

DATA_DIR = "data"

_OC_COLS = [
    "timestamp", "symbol", "expiry", "strike", "option_type",
    "spot", "ltp",
    "volume", "oi", "oi_chg", "iv",
    "delta", "gamma", "theta", "vega", "rho",
]

_MARKET_OPEN  = (9, 15)   # NSE opens 09:15 IST
_MARKET_CLOSE = (15, 30)  # NSE closes 15:30 IST


def _is_market_hours() -> bool:
    now = datetime.now(IST)
    if now.weekday() >= 5:
        return False
    hm = (now.hour, now.minute)
    return _MARKET_OPEN <= hm <= _MARKET_CLOSE


def _parquet_path(date_prefix: str) -> str:
    return os.path.join(DATA_DIR, f"option_chain_{date_prefix}.parquet")


def _last_snapshot_age_mins(date_prefix: str) -> float:
    """Return minutes since the last stored snapshot for today, or inf if none."""
    path = _parquet_path(date_prefix)
    if not os.path.exists(path):
        return float("inf")
    try:
        df = pd.read_parquet(path, columns=["timestamp"])
        if df.empty:
            return float("inf")
        last_ts = df["timestamp"].max()
        last = datetime.strptime(str(last_ts), "%Y%m%d%H%M").replace(tzinfo=IST)
        return (datetime.now(IST) - last).total_seconds() / 60
    except Exception:
        return float("inf")


def insert_option_data(db: str, symbol: str, df: pd.DataFrame, spot: float) -> None:
    """
    Append a snapshot to the daily parquet file.

    `db` is accepted for API compatibility but ignored — all data goes to parquet.
    """
    if df.empty:
        return
    if not _is_market_hours():
        logger.info("[%s] Outside market hours — skipping insert", symbol)
        return

    now = datetime.now(IST)
    date_prefix = now.strftime("%Y%m%d")
    ts = now.strftime("%Y%m%d%H%M")

    if _last_snapshot_age_mins(date_prefix) < 1:
        logger.info("[%s] Skipping insert — last snapshot < 1 min ago", symbol)
        return

    df = df.copy()
    df["timestamp"] = ts
    df["symbol"]    = symbol
    df["spot"]      = spot

    # Normalise ltp from nse_scraper column name if needed
    if "ltp" not in df.columns and "close" in df.columns:
        df["ltp"] = df["close"]

    for col in _OC_COLS:
        if col not in df.columns:
            df[col] = None

    new_rows = df[_OC_COLS].copy()

    path = _parquet_path(date_prefix)
    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(path):
        try:
            existing = pd.read_parquet(path)
            combined = pd.concat([existing, new_rows], ignore_index=True)
        except Exception:
            logger.warning("Could not read existing parquet — overwriting: %s", path)
            combined = new_rows
    else:
        combined = new_rows

    combined = combined.drop_duplicates(
        subset=["timestamp", "strike", "option_type", "expiry"]
    ).sort_values("timestamp").reset_index(drop=True)

    combined.to_parquet(path, index=False)
    logger.info("[%s] Stored %d rows → %s", symbol, len(new_rows), path)


def list_available_dates() -> list[str]:
    """Return sorted list of date strings (YYYYMMDD) that have a parquet file."""
    if not os.path.exists(DATA_DIR):
        return []
    dates = []
    for fname in os.listdir(DATA_DIR):
        if fname.startswith("option_chain_") and fname.endswith(".parquet"):
            date_part = fname[len("option_chain_"):-len(".parquet")]
            if len(date_part) == 8 and date_part.isdigit():
                dates.append(date_part)
    return sorted(dates)


def load_day(date_prefix: str) -> pd.DataFrame:
    """Load all rows for a given date from its parquet file."""
    path = _parquet_path(date_prefix)
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_parquet(path)
