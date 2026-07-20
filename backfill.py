"""
backfill.py — Backfill last 14 trading days of EOD option chain data from NSE bhav copy.
Run once from project root: py backfill.py
"""
import logging
import os
import sqlite3
import sys
from datetime import date, datetime, timedelta

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

OPTION_DB     = os.getenv("OPTION_DB", "data/option_chain.db")
BACKFILL_DAYS = 14

_NSE_SYMBOLS = ["NIFTY50", "BANKNIFTY", "FINNIFTY", "MIDCAPNIFTY"]
_SYM_MAP = {
    "NIFTY50":     "NIFTY",
    "BANKNIFTY":   "BANKNIFTY",
    "FINNIFTY":    "FINNIFTY",
    "MIDCAPNIFTY": "MIDCPNIFTY",
}
_OC_TABLES = {
    "NIFTY50":     "nifty50_option_chain",
    "BANKNIFTY":   "banknifty_option_chain",
    "MIDCAPNIFTY": "midcapnifty_option_chain",
    "FINNIFTY":    "finnifty_option_chain",
}
_INDEX_LABEL = {
    "NIFTY50":     "Nifty50",
    "BANKNIFTY":   "BankNifty",
    "MIDCAPNIFTY": "MidcapNifty",
    "FINNIFTY":    "FinNifty",
}
_OC_COLS = [
    "index_name", "timestamp", "option_type", "expiry", "strike", "spot",
    "ltp", "open", "high", "low", "close", "volume", "oi", "oi_chg",
    "iv", "delta", "gamma", "theta", "vega", "rho",
]


def _last_n_trading_days(n: int):
    days, d = [], date.today() - timedelta(days=1)
    while len(days) < n:
        if d.weekday() < 5:
            days.append(d)
        d -= timedelta(days=1)
    return days


def _already_stored(conn, table: str, ts: str) -> bool:
    row = conn.execute(f"SELECT COUNT(*) FROM {table} WHERE timestamp = ?", (ts,)).fetchone()
    return row[0] > 0


def _spot_from_bhav(bhav: pd.DataFrame, nse_sym: str) -> float:
    """Derive spot from bhav underlying price column."""
    sub = bhav[bhav["TckrSymb"] == nse_sym]
    for col in ("UndrlygPric", "UnderlyingValue"):
        if col in sub.columns:
            v = pd.to_numeric(sub[col], errors="coerce").dropna()
            if not v.empty:
                return float(v.iloc[0])
    return 0.0


def _insert_df(conn, symbol: str, df: pd.DataFrame, spot: float, ts: str):
    table = _OC_TABLES[symbol]
    df = df.copy()
    df["index_name"] = _INDEX_LABEL[symbol]
    df["timestamp"]  = ts
    df["spot"]       = spot
    for col in _OC_COLS:
        if col not in df.columns:
            df[col] = None
    sql = (
        f"INSERT OR IGNORE INTO {table} ({', '.join(_OC_COLS)}) "
        f"VALUES ({', '.join(['?'] * len(_OC_COLS))})"
    )
    conn.executemany(sql, df[_OC_COLS].values.tolist())
    conn.commit()
    logger.info("[%s] Inserted %d rows for ts=%s", symbol, len(df), ts)


def main():
    from src.database import init_db
    init_db(OPTION_DB)

    from nselib import derivatives
    from src.option_chain.nse_scraper import _parse_bhav

    trading_days = _last_n_trading_days(BACKFILL_DAYS)
    logger.info("Backfilling %d trading days: %s → %s",
                len(trading_days), trading_days[-1], trading_days[0])

    conn = sqlite3.connect(OPTION_DB)

    for trade_date in trading_days:
        ds = trade_date.strftime("%d-%m-%Y")
        ts = trade_date.strftime("%Y%m%d") + "1530"

        try:
            bhav = derivatives.fno_bhav_copy(ds)
        except Exception as e:
            logger.warning("bhav fetch failed for %s: %s", ds, e)
            continue

        if bhav is None or bhav.empty:
            logger.warning("No bhav data for %s, skipping", ds)
            continue

        logger.info("Processing %s (%d bhav rows)", ds, len(bhav))

        for symbol in _NSE_SYMBOLS:
            table   = _OC_TABLES[symbol]
            nse_sym = _SYM_MAP[symbol]

            if _already_stored(conn, table, ts):
                logger.info("[%s] %s already in DB, skipping", symbol, ts)
                continue

            sub = bhav[(bhav["TckrSymb"] == nse_sym) & bhav["OptnTp"].notna()]
            if sub.empty:
                logger.warning("[%s] No rows in bhav for %s", symbol, ds)
                continue

            expiry_dates = sorted(sub["XpryDt"].astype(str).str[:10].unique())
            spot         = _spot_from_bhav(bhav, nse_sym)

            all_rows = []
            for exp_iso in expiry_dates:
                try:
                    exp_str = datetime.strptime(exp_iso, "%Y-%m-%d").strftime("%d-%b-%Y")
                except Exception:
                    continue
                df = _parse_bhav(bhav, nse_sym, exp_str, spot)
                if not df.empty:
                    all_rows.append(df)

            if not all_rows:
                logger.warning("[%s] No parsed rows for %s", symbol, ds)
                continue

            combined = pd.concat(all_rows, ignore_index=True)
            _insert_df(conn, symbol, combined, spot, ts)

    conn.close()
    logger.info("Backfill complete.")


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(__file__))
    main()
