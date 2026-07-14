"""database.py — SQLite helpers for market_data.db and option_chain.db."""
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
import pytz

logger = logging.getLogger(__name__)
IST = pytz.timezone("Asia/Kolkata")

# ── Market data ───────────────────────────────────────────────────────────────
_MARKET_COLS = [
    "datetime", "stock_name",
    "open", "high", "low", "close", "volume",
    "sma_5", "sma_10", "sma_20", "sma_50", "sma_100", "sma_200",
    "ema_5", "ema_10", "ema_20", "ema_50", "ema_100", "ema_200",
    "wma_10", "wma_20",
    "macd", "macd_signal", "macd_diff",
    "adx", "adx_pos", "adx_neg",
    "aroon_up", "aroon_down", "aroon_indicator",
    "cci", "dpo", "mass_index",
    "ichimoku_a", "ichimoku_b", "ichimoku_base", "ichimoku_conv",
    "psar", "stc", "trix",
    "vortex_pos", "vortex_neg",
    "kc_upper", "kc_middle", "kc_lower",
    "dc_upper", "dc_middle", "dc_lower",
    "atr",
    "bb_upper", "bb_middle", "bb_lower", "bb_pband", "bb_wband",
    "ulcer_index",
    "rsi_7", "rsi_14", "rsi_21",
    "stoch_k", "stoch_d",
    "roc", "williams_r",
    "awesome_oscillator", "kama",
    "ppo", "tsi", "ultimate_oscillator",
    "obv", "cmf", "acc_dist", "mfi",
    "force_index", "eom", "vpt", "nvi", "vwap",
    "price_change_pct",
    "pivot", "pivot_r1", "pivot_r2", "pivot_r3",
    "pivot_s1", "pivot_s2", "pivot_s3",
    "signal", "updated_at",
]

_MARKET_DDL = """
CREATE TABLE IF NOT EXISTS indexes (
    datetime TEXT, stock_name TEXT,
    open REAL, high REAL, low REAL, close REAL, volume REAL,
    sma_5 REAL, sma_10 REAL, sma_20 REAL, sma_50 REAL, sma_100 REAL, sma_200 REAL,
    ema_5 REAL, ema_10 REAL, ema_20 REAL, ema_50 REAL, ema_100 REAL, ema_200 REAL,
    wma_10 REAL, wma_20 REAL,
    macd REAL, macd_signal REAL, macd_diff REAL,
    adx REAL, adx_pos REAL, adx_neg REAL,
    aroon_up REAL, aroon_down REAL, aroon_indicator REAL,
    cci REAL, dpo REAL, mass_index REAL,
    ichimoku_a REAL, ichimoku_b REAL, ichimoku_base REAL, ichimoku_conv REAL,
    psar REAL, stc REAL, trix REAL,
    vortex_pos REAL, vortex_neg REAL,
    kc_upper REAL, kc_middle REAL, kc_lower REAL,
    dc_upper REAL, dc_middle REAL, dc_lower REAL,
    atr REAL,
    bb_upper REAL, bb_middle REAL, bb_lower REAL, bb_pband REAL, bb_wband REAL,
    ulcer_index REAL,
    rsi_7 REAL, rsi_14 REAL, rsi_21 REAL,
    stoch_k REAL, stoch_d REAL,
    roc REAL, williams_r REAL,
    awesome_oscillator REAL, kama REAL,
    ppo REAL, tsi REAL, ultimate_oscillator REAL,
    obv REAL, cmf REAL, acc_dist REAL, mfi REAL,
    force_index REAL, eom REAL, vpt REAL, nvi REAL, vwap REAL,
    price_change_pct REAL,
    pivot      REAL,
    pivot_r1   REAL,
    pivot_r2   REAL,
    pivot_r3   REAL,
    pivot_s1   REAL,
    pivot_s2   REAL,
    pivot_s3   REAL,
    signal TEXT, updated_at TEXT,
    PRIMARY KEY (datetime, stock_name)
)
"""

# ── Option chain: 4 tables, one per index ─────────────────────────────────────
# Column order as requested:
#   index_name | timestamp(yyyyMMddHHmm) | option_type | expiry |
#   strike | spot | ltp | open | high | low | close |
#   volume | oi | oi_chg | iv | delta | gamma | theta | vega | rho

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
    "index_name",   # Nifty50 / BankNifty / MidcapNifty / FinNifty
    "timestamp",    # yyyyMMddHHmm  e.g. 202606241415
    "option_type",  # CE or PE
    "expiry",       # 30-Jun-2026
    "strike",       # 24000.0
    "spot",         # underlying spot price
    "ltp",          # last traded price
    "open",
    "high",
    "low",
    "close",
    "volume",
    "oi",           # open interest
    "oi_chg",       # change in OI
    "iv",           # implied volatility %
    "delta",
    "gamma",
    "theta",
    "vega",
    "rho",
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

# Market hours IST
_MARKET_OPEN  = "09:15"
_MARKET_CLOSE = "15:45"

_PIVOT_COLS = ("pivot", "pivot_r1", "pivot_r2", "pivot_r3", "pivot_s1", "pivot_s2", "pivot_s3")


def _fetch_existing_pivots(db: str, symbol: str, trade_date: str) -> dict:
    """
    Return pivot values already stored in DB for symbol+date.
    Returns empty dict if none found.
    """
    try:
        with sqlite3.connect(db) as conn:
            row = conn.execute(
                """
                SELECT pivot, pivot_r1, pivot_r2, pivot_r3,
                       pivot_s1, pivot_s2, pivot_s3
                FROM indexes
                WHERE stock_name = ?
                  AND substr(datetime,1,8) = ?
                  AND pivot IS NOT NULL
                LIMIT 1
                """,
                (symbol, trade_date.replace("-", "")),
            ).fetchone()
        if row:
            return dict(zip(_PIVOT_COLS, row))
    except Exception:
        logger.exception("_fetch_existing_pivots failed for %s", symbol)
    return {}




def init_db(market_db: str, option_db: str) -> None:
    """Create all tables if they don't exist, and migrate pivot columns if needed."""
    with sqlite3.connect(market_db) as conn:
        conn.execute(_MARKET_DDL)
        # Migrate: add pivot columns to existing databases that predate this feature
        existing = {row[1] for row in conn.execute("PRAGMA table_info(indexes)")}
        for col in ("pivot", "pivot_r1", "pivot_r2", "pivot_r3",
                    "pivot_s1", "pivot_s2", "pivot_s3"):
            if col not in existing:
                conn.execute(f"ALTER TABLE indexes ADD COLUMN {col} REAL")
                logger.info("Migrated: added column '%s' to indexes table", col)
        conn.commit()
    with sqlite3.connect(option_db) as conn:
        for table in _OC_TABLES.values():
            conn.execute(_OC_DDL.format(table=table))
        conn.commit()
    logger.info("Databases initialised: %s | %s", market_db, option_db)


def _to_ist_str(series: pd.Series) -> pd.Series:
    dt = pd.to_datetime(series)
    if dt.dt.tz is None:
        dt = dt.dt.tz_localize(IST)
    else:
        dt = dt.dt.tz_convert(IST)
    return dt.dt.strftime("%Y%m%d%H%M")


def _is_market_hours(df: pd.DataFrame) -> pd.Series:
    """Return boolean mask for Mon-Fri 09:15-15:45 IST rows."""
    dt = pd.to_datetime(df["datetime"])
    return (
        (dt.dt.weekday < 5) &
        (dt.dt.strftime("%H:%M") >= _MARKET_OPEN) &
        (dt.dt.strftime("%H:%M") <= _MARKET_CLOSE)
    )


def insert_data(db: str, symbol: str, df: pd.DataFrame) -> None:
    """
    Compute indicators and store all Mon-Fri 09:15-15:45 candles.
    Pivot values already in DB are reused — INSERT OR REPLACE never erases them.
    """
    from src.indicators import compute_indicators
    from src.signals import generate_signal

    df = compute_indicators(df.copy(), db=db, symbol=symbol)
    df["stock_name"] = symbol
    df["datetime"]   = _to_ist_str(df["datetime"])
    df["volume"]     = df["volume"].fillna(0)
    df["updated_at"] = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S IST")

    df = df[_is_market_hours(df)].copy()
    if df.empty:
        logger.warning("[%s] No market-hours candles to store", symbol)
        return

    df["signal"] = df.apply(generate_signal, axis=1)

    # ── Protect existing pivot values from being overwritten by NULL ──────────
    # Group by trading date and stamp DB-cached pivots onto rows that have NULL
    dt_series = pd.to_datetime(df["datetime"])
    for trade_date in dt_series.dt.strftime("%Y-%m-%d").unique():
        existing = _fetch_existing_pivots(db, symbol, trade_date)
        if existing:
            mask = dt_series.dt.strftime("%Y%m%d") == trade_date.replace("-", "")  # match yyyyMMdd prefix
            for col, val in existing.items():
                # Only fill NULLs — never overwrite a freshly computed value
                null_mask = mask & df[col].isna()
                df.loc[null_mask, col] = val
            logger.debug("[%s] Reused DB pivots for %s", symbol, trade_date)

    for col in _MARKET_COLS:
        if col not in df.columns:
            df[col] = None

    sql = (
        f"INSERT OR REPLACE INTO indexes ({', '.join(_MARKET_COLS)}) "
        f"VALUES ({', '.join(['?'] * len(_MARKET_COLS))})"
    )
    with sqlite3.connect(db) as conn:
        conn.executemany(sql, df[_MARKET_COLS].values.tolist())
        conn.commit()
    logger.info("[%s] Stored %d candles", symbol, len(df))


def latest_row(db: str, symbol: str) -> Optional[pd.Series]:
    """Return the most recent row for a symbol (prefers rows with volume > 0)."""
    try:
        with sqlite3.connect(db) as conn:
            df = pd.read_sql_query(
                "SELECT * FROM indexes WHERE stock_name=? ORDER BY datetime DESC LIMIT 10",
                conn, params=(symbol,),
            )
        if df.empty:
            return None
        with_vol = df[df["volume"] > 0]
        return with_vol.iloc[0] if not with_vol.empty else df.iloc[0]
    except Exception:
        logger.exception("latest_row failed for %s", symbol)
        return None


def prune_old_option_data(db: str, keep_days: int = 14) -> None:
    """Delete option chain rows older than keep_days from all tables."""
    cutoff = (datetime.now(IST) - timedelta(days=keep_days)).strftime("%Y%m%d%H%M")
    with sqlite3.connect(db) as conn:
        for table in _OC_TABLES.values():
            conn.execute(f"DELETE FROM {table} WHERE timestamp < ?", (cutoff,))
        conn.commit()
    logger.info("Pruned option chain rows older than %d days (cutoff ts=%s)", keep_days, cutoff)


def _update_ohlc(conn: sqlite3.Connection, table: str, today: str) -> None:
    """
    Recompute OHLC for every row inserted today.

    Each row represents a point-in-time snapshot, so:
    - close = this row's own ltp  (plain UPDATE, no FROM — avoids SQLite join ambiguity)
    - open  = ltp of the first snapshot of the day for this contract
    - high  = max ltp across all snapshots UP TO AND INCLUDING this row's timestamp
    - low   = min ltp (>0) across all snapshots UP TO AND INCLUDING this row's timestamp
    """
    # close must be set in a separate statement with no FROM clause.
    # In SQLite's UPDATE...FROM, table.col inside SET resolves against the
    # joined row, not the row being updated, so close would get the last
    # joined ltp instead of each row's own ltp.
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


def insert_option_data(db: str, symbol: str, df: pd.DataFrame, spot: float = 0.0, trade_date: Optional[str] = None) -> None:
    """
    Insert option chain snapshot and recompute intraday OHLC from all
    snapshots stored today for each (option_type, expiry, strike).
    """
    table = _OC_TABLES.get(symbol)
    if not table:
        logger.warning("No option chain table for symbol: %s", symbol)
        return

    # Guard: skip weekends and outside market hours
    now = datetime.now(IST)
    if now.weekday() >= 5:
        logger.info("Weekend (%s) — skipping option chain insert for %s", now.strftime("%A"), symbol)
        return
    hm = now.hour * 100 + now.minute
    if not (915 <= hm <= 1530):
        logger.info("Outside market hours (%s %02d:%02d IST) skipping option chain insert",
                    now.strftime("%a"), now.hour, now.minute)
        return

    ts    = now.strftime("%Y%m%d%H%M")
    today = now.strftime("%Y%m%d")

    label = _INDEX_LABEL.get(symbol, symbol)
    df    = df.copy()
    df["index_name"] = label
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
        # Recompute open/high/low/close for all today's rows from accumulated snapshots
        _update_ohlc(conn, table, today)
        conn.commit()
    inserted = after - before
    logger.info("[%s] ts=%s inserted=%d duplicates=%d | OHLC updated for %s",
                symbol, ts, inserted, len(df) - inserted, today)
