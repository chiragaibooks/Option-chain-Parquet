"""database.py — SQLite helpers for option_chain.db."""
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
import pytz

logger = logging.getLogger(__name__)
IST = pytz.timezone("Asia/Kolkata")

_OC_TABLES = {
    "NIFTY50":     "nifty50_option_chain",
    "BANKNIFTY":   "banknifty_option_chain",
    "MIDCAPNIFTY": "midcapnifty_option_chain",
    "FINNIFTY":    "finnifty_option_chain",
    "SENSEX":      "sensex_option_chain",
}

_INDEX_LABEL = {
    "NIFTY50":     "Nifty50",
    "BANKNIFTY":   "BankNifty",
    "MIDCAPNIFTY": "MidcapNifty",
    "FINNIFTY":    "FinNifty",
    "SENSEX":      "Sensex",
}

_OC_COLS = [
    "index_name", "timestamp", "option_type", "expiry",
    "strike", "spot", "ltp", "open", "high", "low", "close",
    "volume", "oi", "oi_chg", "iv",
    "delta", "gamma", "theta", "vega", "rho",
]

_OC_DDL = """
CREATE TABLE IF NOT EXISTS {table} (
    index_name   TEXT,
    timestamp    TEXT,
    option_type  TEXT,
    expiry       TEXT,
    strike       REAL,
    spot         REAL,
    ltp          REAL,
    open         REAL,
    high         REAL,
    low          REAL,
    close        REAL,
    volume       REAL,
    oi           REAL,
    oi_chg       REAL,
    iv           REAL,
    delta        REAL,
    gamma        REAL,
    theta        REAL,
    vega         REAL,
    rho          REAL,
    PRIMARY KEY (timestamp, option_type, expiry, strike)
)
"""

_MARKET_OPEN  = 915
_MARKET_CLOSE = 1530


def init_db(option_db: str) -> None:
    """Create all option chain tables if they don't exist."""
    with sqlite3.connect(option_db) as conn:
        for table in _OC_TABLES.values():
            conn.execute(_OC_DDL.format(table=table))
        conn.commit()
    logger.info("Option chain DB initialised: %s", option_db)


def _update_ohlc(conn: sqlite3.Connection, table: str, today: str) -> None:
    """
    Recompute OHLC for every row inserted today.
    - close = this row's own ltp
    - open  = ltp of the first snapshot of the day for this contract
    - high  = max ltp across all snapshots up to and including this row
    - low   = min ltp (>0) across all snapshots up to and including this row
    """
    conn.execute(f"""
        UPDATE {table}
        SET close = ltp
        WHERE substr(timestamp,1,8) = ?
    """, (today,))

    conn.execute(f"""
        UPDATE {table}
        SET
            open = day_open.first_ltp,
            high = (
                SELECT MAX(s.ltp)
                FROM {table} s
                WHERE s.option_type = {table}.option_type
                  AND s.expiry      = {table}.expiry
                  AND s.strike      = {table}.strike
                  AND substr(s.timestamp,1,8) = ?
                  AND s.timestamp  <= {table}.timestamp
            ),
            low  = (
                SELECT MIN(s.ltp)
                FROM {table} s
                WHERE s.option_type = {table}.option_type
                  AND s.expiry      = {table}.expiry
                  AND s.strike      = {table}.strike
                  AND substr(s.timestamp,1,8) = ?
                  AND s.timestamp  <= {table}.timestamp
                  AND s.ltp > 0
            )
        FROM (
            SELECT option_type, expiry, strike, ltp AS first_ltp
            FROM (
                SELECT option_type, expiry, strike, ltp,
                       ROW_NUMBER() OVER (
                           PARTITION BY option_type, expiry, strike
                           ORDER BY timestamp ASC
                       ) AS rn
                FROM {table}
                WHERE substr(timestamp,1,8) = ?
            ) ranked
            WHERE rn = 1
        ) day_open
        WHERE {table}.option_type = day_open.option_type
          AND {table}.expiry      = day_open.expiry
          AND {table}.strike      = day_open.strike
          AND substr({table}.timestamp,1,8) = ?
    """, (today, today, today, today))
    logger.debug("[%s] OHLC recomputed for %s", table, today)


def _update_greeks(conn: sqlite3.Connection, table: str, today: str) -> None:
    """Backfill NULL Greeks for today's rows where iv, spot, strike are available."""
    try:
        from src.option_chain.nse_scraper import _greeks
        from datetime import date as _date
    except ImportError:
        return

    rows = conn.execute(f"""
        SELECT timestamp, option_type, expiry, strike, spot, iv
        FROM {table}
        WHERE substr(timestamp,1,8) = ?
          AND delta IS NULL
          AND iv IS NOT NULL AND iv > 0
          AND spot IS NOT NULL AND spot > 0
          AND strike IS NOT NULL AND strike > 0
    """, (today,)).fetchall()

    if not rows:
        return

    updated = 0
    for ts, otype, expiry, strike, spot, iv_pct in rows:
        try:
            exp_date = datetime.strptime(expiry, "%d-%b-%Y").date()
            tte = max((exp_date - _date.today()).days, 0.5) / 365.0
        except Exception:
            continue
        iv_dec = iv_pct / 100.0
        flag   = "c" if otype == "CE" else "p"
        g = _greeks(flag, spot, strike, tte, iv_dec)
        if g["delta"] is None:
            continue
        conn.execute(f"""
            UPDATE {table}
            SET delta=?, gamma=?, theta=?, vega=?, rho=?
            WHERE timestamp=? AND option_type=? AND expiry=? AND strike=?
        """, (g["delta"], g["gamma"], g["theta"], g["vega"], g["rho"],
               ts, otype, expiry, strike))
        updated += 1

    if updated:
        logger.info("[%s] Backfilled Greeks for %d rows on %s", table, updated, today)


def insert_option_data(db: str, symbol: str, df: pd.DataFrame, spot: float = 0.0, trade_date: Optional[str] = None) -> None:
    """Insert option chain snapshot and recompute intraday OHLC."""
    table = _OC_TABLES.get(symbol)
    if not table:
        logger.warning("No option chain table for symbol: %s", symbol)
        return

    now = datetime.now(IST)
    if now.weekday() >= 5:
        logger.info("Weekend — skipping option chain insert for %s", symbol)
        return
    hm = now.hour * 100 + now.minute
    if not (_MARKET_OPEN <= hm <= _MARKET_CLOSE):
        logger.info("Outside market hours (%02d:%02d IST) skipping", now.hour, now.minute)
        return

    ts    = now.strftime("%Y%m%d%H%M")
    today = now.strftime("%Y%m%d")

    df = df.copy()
    df["index_name"] = _INDEX_LABEL.get(symbol, symbol)
    df["timestamp"]  = ts
    df["spot"]       = spot

    for col in _OC_COLS:
        if col not in df.columns:
            df[col] = None

    sql = (
        f"INSERT OR IGNORE INTO {table} ({', '.join(_OC_COLS)}) "
        f"VALUES ({', '.join(['?'] * len(_OC_COLS))})"
    )
    with sqlite3.connect(db) as conn:
        before = conn.execute(f"SELECT COUNT(*) FROM {table} WHERE timestamp=?", (ts,)).fetchone()[0]
        conn.executemany(sql, df[_OC_COLS].values.tolist())
        after  = conn.execute(f"SELECT COUNT(*) FROM {table} WHERE timestamp=?", (ts,)).fetchone()[0]
        _update_ohlc(conn, table, today)
        _update_greeks(conn, table, today)
        conn.commit()
    inserted = after - before
    logger.info("[%s] ts=%s inserted=%d duplicates=%d | OHLC updated",
                symbol, ts, inserted, len(df) - inserted)


def prune_old_option_data(db: str, keep_days: int = 14) -> None:
    """Delete option chain rows older than keep_days."""
    cutoff = (datetime.now(IST) - timedelta(days=keep_days)).strftime("%Y%m%d%H%M")
    with sqlite3.connect(db) as conn:
        for table in _OC_TABLES.values():
            conn.execute(f"DELETE FROM {table} WHERE timestamp < ?", (cutoff,))
        conn.commit()
    logger.info("Pruned option chain rows older than %d days", keep_days)
