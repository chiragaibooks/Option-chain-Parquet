"""
nse_scraper.py
Live     : NSE option chain API (per-minute snapshots)
Fallback : nselib fno_bhav_copy (EOD)
Greeks   : py_vollib (Black-Scholes) — only when vollib is installed AND spot > 0
"""
import logging
import time
import requests
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)

_RISK_FREE = 0.065
_SYM_MAP = {
    "NIFTY50":     "NIFTY",
    "BANKNIFTY":   "BANKNIFTY",
    "FINNIFTY":    "FINNIFTY",
    "MIDCAPNIFTY": "MIDCPNIFTY",
}
_NSE_LIVE_SYM = {
    "NIFTY50":     "NIFTY%2050",
    "BANKNIFTY":   "BANKNIFTY",
    "FINNIFTY":    "FINNIFTY",
    "MIDCAPNIFTY": "MIDCPNIFTY",
}
_MONTHLY_EXPIRY_SYMS = {"MIDCPNIFTY"}

_NSE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.nseindia.com/option-chain",
}
_BSE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.bseindia.com/",
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _to_float(val) -> Optional[float]:
    """Parse a value to float, return None if missing/invalid."""
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
    """Parse to float, return None if missing or negative."""
    f = _to_float(val)
    return f if (f is not None and f >= 0) else None


def _validate_record(row: dict, source: str) -> bool:
    """
    Validate a parsed option chain record.
    Logs and returns False if invalid.
    """
    strike = row.get("strike")
    if strike is None or not isinstance(strike, (int, float)) or strike <= 0:
        logger.debug("[%s] Skipping record: invalid strike=%s", source, strike)
        return False
    if row.get("option_type") not in ("CE", "PE"):
        logger.debug("[%s] Skipping record: invalid option_type=%s", source, row.get("option_type"))
        return False
    if not row.get("expiry"):
        logger.debug("[%s] Skipping record: missing expiry", source)
        return False
    spot = row.get("spot")
    if spot is None or spot <= 0:
        logger.debug("[%s] Skipping record: invalid spot=%s strike=%s", source, spot, strike)
        return False
    ltp = row.get("ltp")
    if ltp is None or ltp < 0:
        logger.debug("[%s] Skipping record: invalid ltp=%s strike=%s", source, ltp, strike)
        return False
    oi = row.get("oi")
    if oi is not None and oi < 0:
        logger.debug("[%s] Skipping record: negative oi=%s strike=%s", source, oi, strike)
        return False
    vol = row.get("volume")
    if vol is not None and vol < 0:
        logger.debug("[%s] Skipping record: negative volume=%s strike=%s", source, vol, strike)
        return False
    return True


# ── Greeks ────────────────────────────────────────────────────────────────────

def _greeks(flag: str, S: float, K: float, t: float, iv: float) -> dict:
    """
    Compute Black-Scholes Greeks using vollib.
    Returns all None if vollib is not installed or computation fails.
    iv must be in decimal form (e.g. 0.18 for 18%).
    """
    null = {"delta": None, "gamma": None, "theta": None, "vega": None, "rho": None}
    if not (S > 0 and K > 0 and t > 0 and iv > 0):
        return null
    try:
        from vollib.black_scholes.greeks import analytical as ga
        return {
            "delta": round(ga.delta(flag, S, K, t, _RISK_FREE, iv), 4),
            "gamma": round(ga.gamma(flag, S, K, t, _RISK_FREE, iv), 6),
            "theta": round(ga.theta(flag, S, K, t, _RISK_FREE, iv), 4),
            "vega":  round(ga.vega( flag, S, K, t, _RISK_FREE, iv), 4),
            "rho":   round(ga.rho(  flag, S, K, t, _RISK_FREE, iv), 4),
        }
    except ImportError:
        return null
    except Exception:
        return null


def _iv_from_price(flag: str, S: float, K: float, t: float, price: float) -> Optional[float]:
    """Compute IV from market price. Returns None if vollib unavailable or fails."""
    if not (S > 0 and K > 0 and t > 0 and price > 0):
        return None
    try:
        from vollib.black_scholes.implied_volatility import implied_volatility as iv_fn
        iv = iv_fn(price, S, K, t, _RISK_FREE, flag)
        return round(iv, 4) if iv and 0.001 < iv < 20 else None
    except ImportError:
        return None
    except Exception:
        return None


# ── Live NSE option chain ─────────────────────────────────────────────────────

def _nse_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(_NSE_HEADERS)
    try:
        s.get("https://www.nseindia.com", timeout=10)
        time.sleep(1)
        s.get("https://www.nseindia.com/market-data/live-equity-market", timeout=10)
        time.sleep(1)
    except Exception:
        pass
    return s


def _fetch_live_option_chain(symbol: str, spot: float) -> pd.DataFrame:
    """
    Fetch live option chain using nsepython.
    IV is taken directly from API field 'impliedVolatility' (stored as %).
    If API returns 0 or missing IV, stores NULL — never uses a hardcoded default.
    Greeks computed only when vollib is available and IV > 0.
    """
    nse_sym = _NSE_LIVE_SYM.get(symbol, "NIFTY")
    try:
        from nsepython import nse_optionchain_scrapper
        data    = nse_optionchain_scrapper(nse_sym)
        records = data.get("records", {})
        api_spot = _to_float(records.get("underlyingValue"))
        spot     = api_spot if (api_spot and api_spot > 0) else spot
        raw      = records.get("data", [])
        logger.debug("[%s] Live API spot=%.2f, raw contracts=%d", symbol, spot, len(raw))
    except Exception as e:
        logger.warning("[%s] nsepython live fetch failed: %s", symbol, e)
        return pd.DataFrame()

    rows = []
    skipped = 0
    for item in raw:
        expiry = item.get("expiryDate", "")
        strike = _to_float(item.get("strikePrice"))
        if strike is None:
            skipped += 1
            continue
        try:
            tte = max((datetime.strptime(expiry, "%d-%b-%Y").date() - date.today()).days, 1) / 365.0
        except Exception:
            tte = None

        for otype, key in (("CE", "CE"), ("PE", "PE")):
            d = item.get(key, {})
            if not d:
                continue

            ltp    = _to_float_nonneg(d.get("lastPrice"))
            oi     = _to_float_nonneg(d.get("openInterest"))
            chg_oi = _to_float(d.get("changeinOpenInterest"))
            vol    = _to_float_nonneg(d.get("totalTradedVolume"))

            # IV: use API value directly (already in %), store None if 0 or missing
            iv_api = _to_float(d.get("impliedVolatility"))
            iv_pct = iv_api if (iv_api is not None and iv_api > 0) else None
            logger.debug("[%s] strike=%s %s API_IV=%s stored_IV=%s", symbol, strike, otype, iv_api, iv_pct)

            # Greeks: only compute if IV available and vollib installed
            iv_dec = iv_pct / 100 if iv_pct else None
            flag   = "c" if otype == "CE" else "p"
            greeks = (
                _greeks(flag, spot, strike, tte, iv_dec)
                if (iv_dec and tte and spot > 0 and ltp and ltp > 0)
                else {"delta": None, "gamma": None, "theta": None, "vega": None, "rho": None}
            )

            record = {
                "expiry":      expiry,
                "strike":      strike,
                "option_type": otype,
                "spot":        spot,
                "ltp":         ltp if ltp is not None else 0.0,
                "open":        None,  # live API does not provide OHLC
                "high":        None,
                "low":         None,
                "close":       None,
                "volume":      vol,
                "oi":          oi,
                "oi_chg":      chg_oi,
                "iv":          iv_pct,   # % or None — never hardcoded 18
                **greeks,
            }
            if _validate_record(record, symbol):
                rows.append(record)
            else:
                skipped += 1

    logger.info("[%s] Live: %d contracts parsed, %d written, %d skipped (spot=%.2f)",
                symbol, len(raw) * 2, len(rows), skipped, spot)
    return pd.DataFrame(rows)


# ── Bhav copy parser ──────────────────────────────────────────────────────────

def _parse_bhav(df: pd.DataFrame, nse_sym: str, expiry_str: str, spot: float) -> pd.DataFrame:
    """
    Parse nselib fno_bhav_copy into standardised option chain format.
    - IV computed via Black-Scholes implied_volatility from LTP; NULL if unavailable.
    - OHLC mapped from bhav fields; NULL if field is NaN.
    - Greeks computed only when IV available; NULL otherwise.
    - No hardcoded default values.
    """
    try:
        exp_date = datetime.strptime(expiry_str, "%d-%b-%Y").date()
    except Exception:
        exp_date = _next_thursday(date.today())
    exp_iso = exp_date.strftime("%Y-%m-%d")

    mask = (
        (df["TckrSymb"] == nse_sym) &
        (df["XpryDt"].astype(str).str[:10] == exp_iso) &
        (df["OptnTp"].notna()) &
        (df["StrkPric"].notna())
    )
    sub = df[mask].copy()
    if sub.empty:
        logger.warning("[%s] No bhav rows for expiry %s", nse_sym, exp_iso)
        return pd.DataFrame()

    tte = max((exp_date - date.today()).days, 1) / 365.0
    rows = []
    skipped = 0

    for _, r in sub.iterrows():
        otype = str(r["OptnTp"]).upper()
        flag  = "c" if otype == "CE" else "p"
        K     = _to_float(r["StrkPric"])

        ltp_val  = _to_float(r.get("LastPric"))
        cls_val  = _to_float(r.get("ClsPric"))
        ltp      = ltp_val if (ltp_val is not None and ltp_val > 0) else cls_val

        oi       = _to_float_nonneg(r.get("OpnIntrst"))
        oi_chg   = _to_float(r.get("ChngInOpnIntrst"))
        vol      = _to_float_nonneg(r.get("TtlTradgVol"))

        # OHLC — use pd.notna to correctly handle NaN from pandas
        open_  = _to_float(r.get("OpnPric"))
        high_  = _to_float(r.get("HghPric"))
        low_   = _to_float(r.get("LwPric"))
        close_ = _to_float(r.get("ClsPric"))

        # IV: compute from LTP via Black-Scholes; NULL if unavailable — no hardcoded default
        iv_dec = _iv_from_price(flag, spot, K, tte, ltp) if (ltp and ltp > 0 and spot > 0 and K) else None
        iv_pct = round(iv_dec * 100, 2) if iv_dec else None
        logger.debug("[%s] strike=%s %s ltp=%.2f computed_IV=%s", nse_sym, K, otype, ltp or 0, iv_pct)

        # Greeks: only when IV available
        greeks = (
            _greeks(flag, spot, K, tte, iv_dec)
            if (iv_dec and spot > 0 and K)
            else {"delta": None, "gamma": None, "theta": None, "vega": None, "rho": None}
        )

        record = {
            "expiry":      expiry_str,
            "strike":      K,
            "option_type": otype,
            "spot":        spot,
            "open":        open_,
            "high":        high_,
            "low":         low_,
            "close":       close_,
            "ltp":         ltp if ltp is not None else 0.0,
            "volume":      vol,
            "oi":          oi,
            "oi_chg":      oi_chg,
            "iv":          iv_pct,   # % or None — never hardcoded 18
            **greeks,
        }
        if _validate_record(record, nse_sym):
            rows.append(record)
        else:
            skipped += 1

    result = pd.DataFrame(rows)
    logger.info("[%s] Bhav: %d rows parsed, %d written, %d skipped (expiry=%s spot=%.2f)",
                nse_sym, len(sub), len(rows), skipped, expiry_str, spot)
    return result


# ── Expiry helpers ────────────────────────────────────────────────────────────

def get_expiry_dates(symbol: str = "NIFTY50") -> List[str]:
    nse_sym = _SYM_MAP.get(symbol, "NIFTY")
    if nse_sym in _MONTHLY_EXPIRY_SYMS:
        return _expiries_from_bhav(nse_sym)
    try:
        from nselib import derivatives
        data     = derivatives.expiry_dates_option_index()
        expiries = data.get(nse_sym, [])
        if expiries:
            logger.info("[%s] nselib expiries: %s", symbol, expiries[:4])
            return expiries
    except Exception:
        logger.warning("[%s] nselib expiry fetch failed", symbol, exc_info=True)
    result, cursor = [], _next_thursday(date.today())
    for _ in range(6):
        result.append(cursor.strftime("%d-%b-%Y"))
        cursor += timedelta(weeks=1)
    return result


def _expiries_from_bhav(nse_sym: str) -> List[str]:
    try:
        from nselib import derivatives
        for i in range(5):
            d = date.today() - timedelta(days=i)
            if d.weekday() >= 5:
                continue
            try:
                bhav = derivatives.fno_bhav_copy(d.strftime("%d-%m-%Y"))
            except Exception:
                continue
            if bhav is None or bhav.empty:
                continue
            sub = bhav[(bhav["TckrSymb"] == nse_sym) & (bhav["OptnTp"].notna())]
            if sub.empty:
                continue
            raw = sorted(sub["XpryDt"].astype(str).str[:10].unique())
            result = []
            for r in raw:
                try:
                    result.append(datetime.strptime(r, "%Y-%m-%d").strftime("%d-%b-%Y"))
                except Exception:
                    pass
            if result:
                logger.info("[%s] bhav expiries: %s", nse_sym, result)
                return result
    except Exception:
        logger.warning("bhav expiry fetch failed for %s", nse_sym, exc_info=True)
    return []


def _next_thursday(ref: date) -> date:
    days = (3 - ref.weekday()) % 7
    return ref + timedelta(days=max(days, 1))


def _get_last_trade_date() -> str:
    d = date.today()
    if d.weekday() >= 5:
        d -= timedelta(days=d.weekday() - 4)
    return d.strftime("%d-%m-%Y")


# ── fetch_option_chain ────────────────────────────────────────────────────────

def fetch_option_chain(
    symbol: str,
    expiry: str,
    spot: float,
    trade_date: Optional[str] = None,
) -> pd.DataFrame:
    df_live = _fetch_live_option_chain(symbol, spot)
    if not df_live.empty:
        df_exp = df_live[df_live["expiry"] == expiry].copy() if expiry else df_live
        if not df_exp.empty:
            return df_exp

    logger.info("[%s] Falling back to bhav copy", symbol)
    nse_sym = _SYM_MAP.get(symbol, "NIFTY")
    if not trade_date:
        d = date.today()
        if d.weekday() >= 5:
            d -= timedelta(days=d.weekday() - 4)
        for i in range(5):
            candidate = d - timedelta(days=i)
            if candidate.weekday() < 5:
                trade_date = candidate.strftime("%d-%m-%Y")
                break

    from nselib import derivatives
    bhav = None
    for i in range(5):
        try_date = (datetime.strptime(trade_date, "%d-%m-%Y").date() - timedelta(days=i))
        if try_date.weekday() >= 5:
            continue
        ds = try_date.strftime("%d-%m-%Y")
        try:
            logger.info("[%s] Trying bhav copy for %s", symbol, ds)
            b = derivatives.fno_bhav_copy(ds)
            if b is not None and not b.empty:
                bhav = b
                break
        except Exception:
            logger.warning("[%s] bhav failed for %s", symbol, ds, exc_info=True)

    if bhav is not None:
        df = _parse_bhav(bhav, nse_sym, expiry, spot)
        if not df.empty:
            return df

    logger.error("[%s] All option chain sources failed", symbol)
    return pd.DataFrame()


# ── BSE SENSEX ────────────────────────────────────────────────────────────────

def fetch_sensex_option_chain(spot: float) -> pd.DataFrame:
    try:
        s = requests.Session()
        s.headers.update(_BSE_HEADERS)
        s.get("https://www.bseindia.com", timeout=10)
        time.sleep(1)
        url  = "https://api.bseindia.com/BseIndiaAPI/api/getOptionChain/w?scripcode=BSE_SENSEX&expirydate=&optiontype=&strikeprice="
        data = s.get(url, timeout=15).json()
        rows = []
        skipped = 0
        for item in data.get("optionChain", []):
            expiry_raw = item.get("ExpiryDate", "")
            try:
                expiry = datetime.strptime(expiry_raw[:10], "%Y-%m-%d").strftime("%d-%b-%Y")
                tte    = max((datetime.strptime(expiry, "%d-%b-%Y").date() - date.today()).days, 1) / 365.0
            except Exception:
                continue
            strike = _to_float(item.get("StrikePrice"))
            if strike is None:
                continue
            for otype, ltp_k, oi_k, vol_k, iv_k, oichg_k in [
                ("CE", "CallLTP", "CallOI", "CallVolume", "CallIV", "CallOIChange"),
                ("PE", "PutLTP",  "PutOI",  "PutVolume",  "PutIV",  "PutOIChange"),
            ]:
                ltp    = _to_float_nonneg(item.get(ltp_k))
                oi     = _to_float_nonneg(item.get(oi_k))
                vol    = _to_float_nonneg(item.get(vol_k))
                oi_chg = _to_float(item.get(oichg_k))
                iv_api = _to_float(item.get(iv_k))
                iv_pct = iv_api if (iv_api is not None and iv_api > 0) else None
                iv_dec = iv_pct / 100 if iv_pct else None
                flag   = "c" if otype == "CE" else "p"
                greeks = (
                    _greeks(flag, spot, strike, tte, iv_dec)
                    if (iv_dec and spot > 0 and ltp and ltp > 0)
                    else {"delta": None, "gamma": None, "theta": None, "vega": None, "rho": None}
                )
                record = {
                    "expiry": expiry, "strike": strike, "option_type": otype,
                    "spot": spot, "ltp": ltp if ltp is not None else 0.0,
                    "open": None, "high": None, "low": None, "close": None,
                    "volume": vol, "oi": oi, "oi_chg": oi_chg,
                    "iv": iv_pct, **greeks,
                }
                if _validate_record(record, "SENSEX"):
                    rows.append(record)
                else:
                    skipped += 1
        df = pd.DataFrame(rows)
        logger.info("[SENSEX] BSE live: %d written, %d skipped (spot=%.2f)", len(rows), skipped, spot)
        return df
    except Exception as e:
        logger.warning("[SENSEX] BSE fetch failed: %s", e)
        return pd.DataFrame()


def get_sensex_expiry_dates() -> List[str]:
    try:
        s = requests.Session()
        s.headers.update(_BSE_HEADERS)
        s.get("https://www.bseindia.com", timeout=10)
        time.sleep(1)
        url  = "https://api.bseindia.com/BseIndiaAPI/api/getOptionChain/w?scripcode=BSE_SENSEX&expirydate=&optiontype=&strikeprice="
        data = s.get(url, timeout=15).json()
        expiries = sorted(set(
            datetime.strptime(item["ExpiryDate"][:10], "%Y-%m-%d").strftime("%d-%b-%Y")
            for item in data.get("optionChain", [])
            if item.get("ExpiryDate")
        ), key=lambda e: datetime.strptime(e, "%d-%b-%Y"))
        today    = date.today()
        upcoming = [e for e in expiries if datetime.strptime(e, "%d-%b-%Y").date() >= today]
        return upcoming[:4]
    except Exception as e:
        logger.warning("[SENSEX] expiry fetch failed: %s", e)
        result, cursor = [], date.today()
        while len(result) < 4:
            cursor += timedelta(days=1)
            if cursor.weekday() == 4:
                result.append(cursor.strftime("%d-%b-%Y"))
        return result


def get_spot(symbol: str, market_db: str = "data/market_data.db") -> Optional[float]:
    if symbol == "SENSEX":
        try:
            import yfinance as yf
            hist = yf.Ticker("^BSESN").history(period="1d")
            if not hist.empty:
                return float(hist["Close"].iloc[-1])
        except Exception:
            pass

    try:
        from nselib import capital_market
        data = capital_market.index_data()
        if data is not None and not data.empty:
            sym_map_display = {
                "NIFTY50":     "NIFTY 50",
                "BANKNIFTY":   "NIFTY BANK",
                "FINNIFTY":    "NIFTY FIN SERVICE",
                "MIDCAPNIFTY": "NIFTY MIDCAP SELECT",
            }
            label = sym_map_display.get(symbol, "")
            row   = data[data["indexSymbol"] == label] if "indexSymbol" in data.columns else pd.DataFrame()
            if not row.empty:
                return float(row.iloc[0]["last"])
    except Exception:
        pass

    try:
        import sqlite3
        with sqlite3.connect(market_db) as conn:
            row = conn.execute(
                "SELECT close FROM indexes WHERE stock_name=? ORDER BY datetime DESC LIMIT 1",
                (symbol,)
            ).fetchone()
            if row:
                logger.info("[%s] spot from market_data.db: %.2f", symbol, row[0])
                return float(row[0])
    except Exception:
        pass
    return None
