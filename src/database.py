"""database.py — SQLite helpers for market_data.db."""
import sqlite3
import logging
from datetime import datetime
from typing import Optional

import pandas as pd
import pytz

logger = logging.getLogger(__name__)
IST = pytz.timezone("Asia/Kolkata")

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
    pivot REAL, pivot_r1 REAL, pivot_r2 REAL, pivot_r3 REAL,
    pivot_s1 REAL, pivot_s2 REAL, pivot_s3 REAL,
    signal TEXT, updated_at TEXT,
    PRIMARY KEY (datetime, stock_name)
)
"""

_MARKET_OPEN  = "09:15"
_MARKET_CLOSE = "15:45"
_PIVOT_COLS   = ("pivot", "pivot_r1", "pivot_r2", "pivot_r3", "pivot_s1", "pivot_s2", "pivot_s3")


def init_db(market_db: str) -> None:
    with sqlite3.connect(market_db) as conn:
        conn.execute(_MARKET_DDL)
        existing = {row[1] for row in conn.execute("PRAGMA table_info(indexes)")}
        for col in _PIVOT_COLS:
            if col not in existing:
                conn.execute(f"ALTER TABLE indexes ADD COLUMN {col} REAL")
                logger.info("Migrated: added column '%s'", col)
        conn.commit()
    logger.info("Database initialised: %s", market_db)


def _to_ist_str(series: pd.Series) -> pd.Series:
    dt = pd.to_datetime(series)
    if dt.dt.tz is None:
        dt = dt.dt.tz_localize(IST)
    else:
        dt = dt.dt.tz_convert(IST)
    return dt.dt.strftime("%Y%m%d%H%M")


def _is_market_hours(df: pd.DataFrame) -> pd.Series:
    dt = pd.to_datetime(df["datetime"])
    return (
        (dt.dt.weekday < 5) &
        (dt.dt.strftime("%H:%M") >= _MARKET_OPEN) &
        (dt.dt.strftime("%H:%M") <= _MARKET_CLOSE)
    )


def _fetch_existing_pivots(db: str, symbol: str, trade_date: str) -> dict:
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


def insert_data(db: str, symbol: str, df: pd.DataFrame) -> None:
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

    dt_series = pd.to_datetime(df["datetime"])
    for trade_date in dt_series.dt.strftime("%Y-%m-%d").unique():
        existing = _fetch_existing_pivots(db, symbol, trade_date)
        if existing:
            mask = dt_series.dt.strftime("%Y%m%d") == trade_date.replace("-", "")
            for col, val in existing.items():
                null_mask = mask & df[col].isna()
                df.loc[null_mask, col] = val

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
