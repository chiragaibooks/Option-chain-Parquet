"""
collect.py — Single-file NIFTY50 option chain collector.

Does everything in one place:
  1. Fetch spot price (yfinance -> nselib fallback)
  2. Fetch expiry dates (nselib -> computed Thursdays fallback)
  3. Scrape live NSE option chain (v3 API -> bhav copy fallback)
  4. Solve IV from LTP when NSE doesn't provide it (Black-Scholes + bisection)
  5. Compute Greeks (delta, gamma, theta, vega, rho)
  6. Store a per-minute snapshot to data/option_chain_YYYYMMDD.parquet
  7. Update README.md with the latest snapshots

Usage:
    python collect.py            # fetch one snapshot and store it
    python collect.py --loop     # keep fetching every 60s until market close
"""
import argparse
import glob
import logging
import math
import os
import sys
import time
from datetime import date, datetime, timedelta
from logging.handlers import RotatingFileHandler
from typing import List, Optional

import pandas as pd
import pytz
import requests
from scipy.stats import norm

# ──────────────────────────────────────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────────────────────────────────────

IST             = pytz.timezone("Asia/Kolkata")
RISK_FREE_RATE  = 0.065                 # RBI repo rate ~6.5%
DATA_DIR        = "data"
LOG_DIR         = "data/logs"
SYMBOL          = "NIFTY50"
NSE_SYMBOL      = "NIFTY"
STRIKE_GAP      = 50
N_EXPIRIES      = 4

MARKET_OPEN     = (9, 15)               # 09:15 IST
MARKET_CLOSE    = (15, 30)              # 15:30 IST

_OC_COLS = [
    "timestamp", "symbol", "expiry", "strike", "option_type",
    "spot", "ltp",
    "volume", "oi", "oi_chg", "iv",
    "delta", "gamma", "theta", "vega", "rho",
]

_NSE_OC_V3_URL = "https://www.nseindia.com/api/option-chain-v3?type={typ}&symbol={sym}&expiry={expiry}"
_NSE_OC_ORIGIN = "https://www.nseindia.com/option-chain"

# ──────────────────────────────────────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────────────────────────────────────

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

_fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
_fh = RotatingFileHandler(os.path.join(LOG_DIR, "app.log"), maxBytes=5 * 1024 * 1024, backupCount=3)
_fh.setFormatter(_fmt)
_ch = logging.StreamHandler(sys.stdout)
_ch.setFormatter(_fmt)
logging.basicConfig(level=logging.INFO, handlers=[_fh, _ch])
logger = logging.getLogger("collect")


# ──────────────────────────────────────────────────────────────────────────────
# Small parse helpers
# ──────────────────────────────────────────────────────────────────────────────

def _to_float(val) -> Optional[float]:
    if val is None:
        return None
    if isinstance(val, float) and pd.isna(val):
        return None
    try:
        f = float(val)
        return f if pd.notna(f) else None
    except (TypeError, ValueError):
        return None


def _to_float_nonneg(val) -> Optional[float]:
    f = _to_float(val)
    return f if (f is not None and f >= 0) else None


# ──────────────────────────────────────────────────────────────────────────────
# Black-Scholes: pricing, IV solver, Greeks
# ──────────────────────────────────────────────────────────────────────────────

def _d1_d2(S: float, K: float, t: float, r: float, iv: float):
    d1 = (math.log(S / K) + (r + 0.5 * iv ** 2) * t) / (iv * math.sqrt(t))
    return d1, d1 - iv * math.sqrt(t)


def bs_price(flag: str, S: float, K: float, t: float, iv: float) -> float:
    """Black-Scholes option price. flag: 'c' = call, 'p' = put."""
    d1, d2 = _d1_d2(S, K, t, RISK_FREE_RATE, iv)
    r = RISK_FREE_RATE
    if flag == "c":
        return S * norm.cdf(d1) - K * math.exp(-r * t) * norm.cdf(d2)
    return K * math.exp(-r * t) * norm.cdf(-d2) - S * norm.cdf(-d1)


def iv_from_price(flag: str, S: float, K: float, t: float, price: float) -> Optional[float]:
    """Bisection IV solver — finds the IV that makes BS price == market price."""
    if not (S > 0 and K > 0 and t > 0 and price > 0):
        return None
    try:
        lo, hi = 0.001, 10.0
        for _ in range(100):
            mid = (lo + hi) / 2
            if hi - lo < 1e-5:
                break
            if bs_price(flag, S, K, t, mid) > price:
                hi = mid
            else:
                lo = mid
        iv = (lo + hi) / 2
        return round(iv, 4) if 0.001 < iv < 10 else None
    except Exception:
        return None


def compute_greeks(S: float, K: float, t: float, iv: float, option_type: str) -> dict:
    """
    Return all five Greeks.
      - delta : CE ∈ (0,1) | PE ∈ (-1,0)
      - gamma : same for CE and PE
      - theta : per calendar day (÷365)
      - vega  : per 1% IV move (÷100)
      - rho   : per 1% rate move (÷100)
    """
    null = {k: None for k in ("delta", "gamma", "theta", "vega", "rho")}
    if not (S and K and t and iv and S > 0 and K > 0 and t > 0 and iv > 0):
        return null
    try:
        r = RISK_FREE_RATE
        d1, d2 = _d1_d2(S, K, t, r, iv)
        pdf_d1 = norm.pdf(d1)
        gamma  = pdf_d1 / (S * iv * math.sqrt(t))
        vega   = S * pdf_d1 * math.sqrt(t) / 100
        t_decay = -(S * pdf_d1 * iv) / (2 * math.sqrt(t))
        disc    = r * K * math.exp(-r * t)
        if option_type == "CE":
            delta = norm.cdf(d1)
            theta = (t_decay - disc * norm.cdf(d2)) / 365
            rho   = K * t * math.exp(-r * t) * norm.cdf(d2) / 100
        else:
            delta = norm.cdf(d1) - 1
            theta = (t_decay + disc * norm.cdf(-d2)) / 365
            rho   = -K * t * math.exp(-r * t) * norm.cdf(-d2) / 100
        return {
            "delta": round(delta, 4),
            "gamma": round(gamma, 6),
            "theta": round(theta, 4),
            "vega":  round(vega, 4),
            "rho":   round(rho, 4),
        }
    except Exception:
        logger.debug("greeks failed for K=%s %s", K, option_type)
        return null


# ──────────────────────────────────────────────────────────────────────────────
# Spot price
# ──────────────────────────────────────────────────────────────────────────────

def get_spot() -> Optional[float]:
    # Try 1: yfinance
    try:
        import yfinance as yf
        ticker = yf.Ticker("^NSEI")
        price = ticker.fast_info.get("lastPrice") or ticker.fast_info.get("regularMarketPrice")
        if price and float(price) > 0:
            logger.info("spot (yfinance): %.2f", float(price))
            return float(price)
    except Exception as e:
        logger.warning("yfinance spot failed: %s", e)

    # Try 2: nselib
    try:
        from nselib import capital_market
        data = capital_market.index_data()
        if data is not None and not data.empty and "indexSymbol" in data.columns:
            row = data[data["indexSymbol"] == "NIFTY 50"]
            if not row.empty:
                return float(row.iloc[0]["last"])
    except Exception as e:
        logger.warning("nselib spot failed: %s", e)

    return None


# ──────────────────────────────────────────────────────────────────────────────
# Expiry dates
# ──────────────────────────────────────────────────────────────────────────────

def _next_thursday(ref: date) -> date:
    days = (3 - ref.weekday()) % 7
    return ref + timedelta(days=max(days, 1))


def get_expiry_dates() -> List[str]:
    try:
        from nselib import derivatives
        data = derivatives.expiry_dates_option_index()
        expiries = data.get(NSE_SYMBOL, [])
        if expiries:
            logger.info("expiries (nselib): %s", expiries[:N_EXPIRIES])
            return expiries
    except Exception:
        logger.warning("nselib expiry fetch failed", exc_info=True)

    # Fallback: next 6 Thursdays
    result, cursor = [], _next_thursday(date.today())
    for _ in range(6):
        result.append(cursor.strftime("%d-%b-%Y"))
        cursor += timedelta(weeks=1)
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Live NSE option chain
# ──────────────────────────────────────────────────────────────────────────────

def fetch_option_chain(spot: float) -> pd.DataFrame:
    """Fetch live NSE option chain for the first N_EXPIRIES expiries."""
    from nselib.libutil import nse_urlfetch

    expiries = get_expiry_dates()[:N_EXPIRIES]
    if not expiries:
        logger.warning("no expiries available")
        return pd.DataFrame()

    all_rows: list = []
    skipped = 0

    for expiry in expiries:
        url = _NSE_OC_V3_URL.format(typ="Indices", sym=NSE_SYMBOL, expiry=expiry)
        try:
            resp    = nse_urlfetch(url, origin_url=_NSE_OC_ORIGIN)
            data    = resp.json()
            records = data.get("records", {})
            api_spot = _to_float(records.get("underlyingValue"))
            use_spot = api_spot if (api_spot and api_spot > 0) else spot
            raw      = records.get("data", [])
            logger.info("expiry=%s status=%d spot=%.2f rows=%d",
                        expiry, resp.status_code, use_spot, len(raw))
        except Exception as e:
            logger.warning("v3 API failed for expiry=%s: %s", expiry, e)
            continue

        try:
            tte = max((datetime.strptime(expiry, "%d-%b-%Y").date() - date.today()).days, 0.5) / 365.0
        except Exception:
            tte = None

        for item in raw:
            strike = _to_float(item.get("strikePrice"))
            if strike is None:
                skipped += 1
                continue
            for otype in ("CE", "PE"):
                d = item.get(otype, {})
                if not d:
                    continue
                ltp    = _to_float_nonneg(d.get("lastPrice"))
                oi     = _to_float_nonneg(d.get("openInterest"))
                chg_oi = _to_float(d.get("changeinOpenInterest"))
                vol    = _to_float_nonneg(d.get("totalTradedVolume"))
                iv_api = _to_float(d.get("impliedVolatility"))
                iv_pct = iv_api if (iv_api is not None and iv_api > 0) else None

                # Fallback: solve IV from LTP if NSE didn't provide it
                if iv_pct is None and ltp and ltp > 0 and tte:
                    flag = "c" if otype == "CE" else "p"
                    iv_dec_fb = iv_from_price(flag, use_spot, strike, tte, ltp)
                    iv_pct = round(iv_dec_fb * 100, 2) if iv_dec_fb else None

                iv_dec = iv_pct / 100 if iv_pct else None
                greeks = (
                    compute_greeks(use_spot, strike, tte, iv_dec, otype)
                    if (iv_dec and tte and use_spot > 0 and strike > 0)
                    else {k: None for k in ("delta", "gamma", "theta", "vega", "rho")}
                )

                record = {
                    "expiry": expiry, "strike": strike, "option_type": otype,
                    "spot": use_spot, "ltp": ltp if ltp is not None else 0.0,
                    "volume": vol, "oi": oi, "oi_chg": chg_oi, "iv": iv_pct,
                    **greeks,
                }
                if _valid(record):
                    all_rows.append(record)
                else:
                    skipped += 1

    logger.info("total: %d rows, %d skipped", len(all_rows), skipped)
    return pd.DataFrame(all_rows)


def _valid(row: dict) -> bool:
    """Reject bad records: bad strike/type/expiry/spot/ltp, negative oi/volume."""
    strike = row.get("strike")
    if strike is None or strike <= 0:
        return False
    if row.get("option_type") not in ("CE", "PE"):
        return False
    if not row.get("expiry"):
        return False
    if not row.get("spot") or row["spot"] <= 0:
        return False
    ltp = row.get("ltp")
    if ltp is None or ltp <= 0:
        return False
    if row.get("oi") is not None and row["oi"] < 0:
        return False
    if row.get("volume") is not None and row["volume"] < 0:
        return False
    return True


# ──────────────────────────────────────────────────────────────────────────────
# Parquet storage
# ──────────────────────────────────────────────────────────────────────────────

def _is_market_hours(now: datetime) -> bool:
    if now.weekday() >= 5:
        return False
    hm = (now.hour, now.minute)
    return MARKET_OPEN <= hm <= MARKET_CLOSE


def _parquet_path(date_prefix: str) -> str:
    return os.path.join(DATA_DIR, f"option_chain_{date_prefix}.parquet")


def _last_snapshot_age_mins(date_prefix: str, now: datetime) -> float:
    path = _parquet_path(date_prefix)
    if not os.path.exists(path):
        return float("inf")
    try:
        df = pd.read_parquet(path, columns=["timestamp"])
        if df.empty:
            return float("inf")
        last = datetime.strptime(str(df["timestamp"].max()), "%Y%m%d%H%M").replace(tzinfo=IST)
        return (now - last).total_seconds() / 60
    except Exception:
        return float("inf")


def store_snapshot(df: pd.DataFrame, spot: float) -> bool:
    """Append one snapshot to today's parquet file. Returns True if stored."""
    if df.empty:
        logger.info("empty dataframe — nothing to store")
        return False

    now = datetime.now(IST)
    if not _is_market_hours(now):
        logger.info("outside market hours — skipping store")
        return False

    date_prefix = now.strftime("%Y%m%d")
    ts = now.strftime("%Y%m%d%H%M")

    if _last_snapshot_age_mins(date_prefix, now) < 1:
        logger.info("last snapshot < 1 min ago — skipping store")
        return False

    df = df.copy()
    df["timestamp"] = ts
    df["symbol"]    = SYMBOL
    df["spot"]      = spot
    for col in _OC_COLS:
        if col not in df.columns:
            df[col] = None
    new_rows = df[_OC_COLS].copy()

    path = _parquet_path(date_prefix)
    if os.path.exists(path):
        try:
            combined = pd.concat([pd.read_parquet(path), new_rows], ignore_index=True)
        except Exception:
            logger.warning("could not read existing parquet — overwriting")
            combined = new_rows
    else:
        combined = new_rows

    combined = (
        combined.drop_duplicates(subset=["timestamp", "strike", "option_type", "expiry"])
        .sort_values("timestamp")
        .reset_index(drop=True)
    )
    combined.to_parquet(path, index=False)
    logger.info("stored %d rows -> %s", len(new_rows), path)
    return True


# ──────────────────────────────────────────────────────────────────────────────
# Outputs: README + dashboard JSON
# ──────────────────────────────────────────────────────────────────────────────

def _fmt_ts(ts: str) -> str:
    try:
        return datetime.strptime(str(ts), "%Y%m%d%H%M").strftime("%d %b %Y %H:%M IST")
    except Exception:
        return str(ts)


def write_readme() -> None:
    files = sorted(glob.glob(os.path.join(DATA_DIR, "option_chain_*.parquet")), reverse=True)
    if not files:
        _write_file("README.md", "# 📋 NIFTY50 Option Chain\n\n_No data yet._\n")
        return

    now_str = datetime.now(IST).strftime("%d %b %Y %H:%M:%S IST")
    content = f"<!-- auto-updated: {now_str} -->\n\n"
    content += "# 📋 NIFTY50 Option Chain — Parquet Data\n\n"
    content += f"**Updated:** {now_str}\n\n---\n\n"
    content += "🔍 **[Open Interactive Dashboard →](https://chiragaibooks.github.io/Option-chain-Parquet/)**\n\n---\n\n"

    try:
        df = pd.read_parquet(files[0])
        latest_ts = df["timestamp"].drop_duplicates().sort_values().tail(10).tolist()
        content += f"## 🕐 Last 10 Snapshots — `{os.path.basename(files[0])}`\n\n"
        for ts in reversed(latest_ts):
            rows = df[df["timestamp"] == ts][["strike", "option_type", "expiry", "ltp"]] \
                .sort_values(["strike", "option_type"]).values.tolist()
            content += f"### {_fmt_ts(ts)}\n\n<table>\n"
            content += "<tr><th>Expiry</th><th>Strike</th><th>Type</th><th>LTP</th></tr>\n"
            for strike, otype, expiry, ltp in rows:
                ltp_s = f"{float(ltp):,.2f}" if ltp is not None else "-"
                content += f"<tr><td>{expiry or '-'}</td><td>{int(strike)}</td><td>{otype}</td><td>{ltp_s}</td></tr>\n"
            content += "</table>\n\n---\n\n"
    except Exception:
        logger.exception("readme snapshot section failed")

    _write_file("README.md", content)
    logger.info("README updated (%d parquet files)", len(files))


def _now_str() -> str:
    return datetime.now(IST).strftime("%d %b %Y %H:%M:%S IST")


def _write_file(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ──────────────────────────────────────────────────────────────────────────────
# Orchestration
# ──────────────────────────────────────────────────────────────────────────────

def run_once() -> bool:
    """One full cycle: spot -> chain -> store -> outputs. Returns True if stored."""
    logger.info("=== fetch cycle start ===")
    spot = get_spot() or 0.0
    if spot <= 0:
        logger.error("could not fetch spot — aborting cycle")
        return False

    df = fetch_option_chain(spot)
    if df.empty:
        logger.error("empty option chain — aborting cycle")
        return False

    stored = store_snapshot(df, spot)
    if stored:
        write_readme()
    logger.info("=== fetch cycle done (stored=%s) ===", stored)
    return stored


def run_loop(interval: int = 60) -> None:
    """Keep fetching every `interval` seconds until market close."""
    logger.info("=== loop mode start ===")
    while True:
        now = datetime.now(IST)
        hm = (now.hour, now.minute)
        if now.weekday() >= 5:
            logger.info("weekend — exiting loop")
            return
        if hm > MARKET_CLOSE:
            logger.info("market closed — exiting loop")
            return
        if hm < MARKET_OPEN:
            wait = ((MARKET_OPEN[0] * 60 + MARKET_OPEN[1]) - (now.hour * 60 + now.minute)) * 60 - now.second
            logger.info("pre-market — sleeping %ds until 09:15", max(wait, 0))
            time.sleep(max(wait, 0))
            continue

        next_run = time.monotonic() + interval
        try:
            run_once()
        except Exception as e:
            logger.error("cycle error: %s", e)
        sleep_for = next_run - time.monotonic()
        if sleep_for > 0:
            time.sleep(sleep_for)


def main() -> None:
    parser = argparse.ArgumentParser(description="NIFTY50 option chain collector")
    parser.add_argument("--loop", action="store_true", help="Loop every 60s until market close")
    args = parser.parse_args()
    if args.loop:
        run_loop()
    else:
        run_once()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("fatal error")
        sys.exit(1)
