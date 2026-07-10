"""
bse_scraper.py — BSE SENSEX option chain fetcher.
Endpoint: GET https://api.bseindia.com/BseIndiaAPI/api/DerivOptionChain_IV/w
scrip_cd=1 → SENSEX

Each row in the response contains both CE (C_* prefix) and PE data for a strike.
"""
import logging
import time
from datetime import date, datetime, timedelta
from typing import List, Optional

import requests
import pandas as pd

from src.option_chain.nse_scraper import _greeks

logger = logging.getLogger(__name__)

_SCRIP_CD   = "1"
_RISK_FREE  = 0.065
_BASE_URL   = "https://api.bseindia.com/BseIndiaAPI/api/DerivOptionChain_IV/w"
_HEADERS    = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept":     "application/json, text/plain, */*",
    "Referer":    "https://www.bseindia.com/",
    "Origin":     "https://www.bseindia.com",
}


def _bse_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(_HEADERS)
    try:
        s.get("https://www.bseindia.com", timeout=10)
        time.sleep(1)
    except Exception:
        pass
    return s


def _fetch_raw(expiry: str, retries: int = 3) -> List[dict]:
    """
    Fetch raw rows from BSE API with exponential backoff.
    expiry format: '30 Jul 2026'
    """
    s = _bse_session()
    params = {"Expiry": expiry, "scrip_cd": _SCRIP_CD, "strprice": "0"}

    for attempt in range(1, retries + 1):
        try:
            logger.info("[SENSEX] GET %s params=%s", _BASE_URL, params)
            r = s.get(_BASE_URL, params=params, timeout=15)
            r.raise_for_status()
            data = r.json()
            rows = data.get("Table", [])
            logger.info(
                "[SENSEX] url=%s | expiry=%s | status=%d | size=%d bytes | rows=%d",
                r.url, expiry, r.status_code, len(r.content), len(rows),
            )
            if rows:
                logger.debug(
                    "[SENSEX] first row SCRIP_ID=%s End_TimeStamp=%s",
                    rows[0].get("SCRIP_ID"), rows[0].get("End_TimeStamp"),
                )
            else:
                logger.warning(
                    "[SENSEX] Empty Table for expiry=%s | full response: %s",
                    expiry, data,
                )
            return rows
        except Exception as e:
            wait = 2 ** attempt
            logger.warning("[SENSEX] Attempt %d/%d failed: %s — retrying in %ds", attempt, retries, e, wait)
            if attempt < retries:
                time.sleep(wait)

    logger.error("[SENSEX] All %d attempts failed for expiry %s", retries, expiry)
    return []


def _parse_float(val) -> Optional[float]:
    """Parse BSE numeric strings like '78,260.64' → 78260.64. Returns None if missing/invalid."""
    if val is None:
        return None
    s = str(val).replace(",", "").strip()
    if s in ("", "NA", "N/A", "-", "null", "None"):
        return None
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def _parse_float_nonneg(val) -> Optional[float]:
    """Parse to float, return None if missing or negative."""
    f = _parse_float(val)
    return f if (f is not None and f >= 0) else None


def _log_iv(index: str, strike, otype: str, expiry: str, raw_iv, parsed_iv, stored_iv, reason: str) -> None:
    logger.debug(
        "Index: %s | Strike: %s | Type: %s | Expiry: %s\n"
        "  Raw API IV: %s | Parsed IV: %s | Stored IV: %s | Reason: %s",
        index, strike, otype, expiry, raw_iv, parsed_iv, stored_iv, reason,
    )


def _fmt_expiry_bse(expiry_str: str) -> str:
    """Convert '30-Jul-2026' → '30 Jul 2026' (zero-padded day) for BSE API."""
    return datetime.strptime(expiry_str, "%d-%b-%Y").strftime("%d %b %Y")


def get_sensex_expiry_dates() -> List[str]:
    """
    Return next 4 SENSEX expiry dates in '%d-%b-%Y' format.
    SENSEX options expire every Thursday on BSE.
    Probes the API with zero-padded Thursday dates ('%d %b %Y') to confirm
    live data exists — only returns expiries that have actual rows.
    """
    s = _bse_session()
    today = date.today()
    expiries: List[str] = []

    # Next 8 Thursdays (weekday=3)
    cursor = today
    candidates: List[tuple] = []  # (bse_fmt '09 Jul 2026', std_fmt '09-Jul-2026')
    while len(candidates) < 8:
        cursor += timedelta(days=1)
        if cursor.weekday() == 3:  # Thursday
            candidates.append((cursor.strftime("%d %b %Y"), cursor.strftime("%d-%b-%Y")))

    logger.info("[SENSEX] Probing %d candidate Thursdays: %s", len(candidates), [c[0] for c in candidates])
    for bse_fmt, std_fmt in candidates:
        try:
            logger.info("[SENSEX] GET %s params=Expiry=%s scrip_cd=%s", _BASE_URL, bse_fmt, _SCRIP_CD)
            r = s.get(_BASE_URL, params={"Expiry": bse_fmt, "scrip_cd": _SCRIP_CD, "strprice": "0"}, timeout=10)
            data = r.json()
            rows = data.get("Table", [])
            logger.info("[SENSEX] probe expiry=%s status=%d rows=%d", bse_fmt, r.status_code, len(rows))
            if rows:
                expiries.append(std_fmt)
                if len(expiries) == 4:
                    break
            time.sleep(0.3)
        except Exception:
            logger.warning("[SENSEX] probe failed for %s", bse_fmt, exc_info=True)

    if expiries:
        logger.info("[SENSEX] Live expiries confirmed: %s", expiries)
        return expiries

    logger.error(
        "[SENSEX] No live data found for any Thursday expiry in: %s",
        [c[0] for c in candidates],
    )
    return []


def fetch_sensex_option_chain(expiry: str, spot: float = 0.0) -> pd.DataFrame:
    """
    Fetch SENSEX option chain from BSE for a given expiry.

    expiry: '%d-%b-%Y' format e.g. '25-Jul-2026'
    Returns DataFrame with columns matching insert_option_data() requirements.
    """
    logger.info("[SENSEX] Fetching BSE option chain for expiry %s...", expiry)

    # Convert expiry to BSE format
    try:
        bse_expiry = _fmt_expiry_bse(expiry)
    except ValueError:
        logger.error("[SENSEX] Invalid expiry format: %s", expiry)
        return pd.DataFrame()

    raw_rows = _fetch_raw(bse_expiry)
    if not raw_rows:
        return pd.DataFrame()

    try:
        exp_date = datetime.strptime(expiry, "%d-%b-%Y").date()
        tte = max((exp_date - date.today()).days, 1) / 365.0
    except Exception:
        tte = 0.1

    rows = []
    for item in raw_rows:
        # Skip non-SENSEX rows (endpoint may return BANKEX too)
        if item.get("SCRIP_ID", "") != "BSX" or item.get("comapny_name", "").strip() != "SENSEX":
            continue

        strike = _parse_float(item.get("Strike_Price1"))
        if not strike:
            continue

        # Use UlaValue as spot if not provided
        item_spot = _parse_float(item.get("UlaValue")) or spot

        # ── PE (no prefix) ────────────────────────────────────────────────────
        pe_ltp    = _parse_float_nonneg(item.get("Last_Trd_Price"))
        pe_oi     = _parse_float_nonneg(item.get("Open_Interest"))
        pe_oi_chg = _parse_float(item.get("Absolute_Change_OI"))
        pe_vol    = _parse_float_nonneg(item.get("Vol_Traded"))
        pe_iv_raw = _parse_float(item.get("IV"))

        if pe_iv_raw is None:
            pe_iv_pct = None
            _log_iv("SENSEX", strike, "PE", expiry, item.get("IV"), None, None, "API did not provide IV")
        elif pe_iv_raw == 0.0:
            pe_iv_pct = 0.0
            _log_iv("SENSEX", strike, "PE", expiry, 0, 0.0, 0.0, "API explicitly returned zero")
        else:
            pe_iv_pct = pe_iv_raw

        pe_iv_dec = pe_iv_pct / 100 if (pe_iv_pct is not None and pe_iv_pct > 0) else None
        pe_greeks = (
            _greeks("p", item_spot, strike, tte, pe_iv_dec)
            if (pe_iv_dec and item_spot > 0 and pe_ltp and pe_ltp > 0)
            else {"delta": None, "gamma": None, "theta": None, "vega": None, "rho": None}
        )

        rows.append({
            "expiry": expiry, "strike": strike, "option_type": "PE",
            "ltp": pe_ltp if pe_ltp is not None else 0.0,
            "volume": pe_vol, "oi": pe_oi, "oi_chg": pe_oi_chg,
            "iv": pe_iv_pct, "spot": item_spot, **pe_greeks,
        })

        # ── CE (C_ prefix) ────────────────────────────────────────────────────
        ce_ltp    = _parse_float_nonneg(item.get("C_Last_Trd_Price"))
        ce_oi     = _parse_float_nonneg(item.get("C_Open_Interest"))
        ce_oi_chg = _parse_float(item.get("C_Absolute_Change_OI"))
        ce_vol    = _parse_float_nonneg(item.get("C_Vol_Traded"))
        ce_iv_raw = _parse_float(item.get("C_IV"))

        if ce_iv_raw is None:
            ce_iv_pct = None
            _log_iv("SENSEX", strike, "CE", expiry, item.get("C_IV"), None, None, "API did not provide IV")
        elif ce_iv_raw == 0.0:
            ce_iv_pct = 0.0
            _log_iv("SENSEX", strike, "CE", expiry, 0, 0.0, 0.0, "API explicitly returned zero")
        else:
            ce_iv_pct = ce_iv_raw

        ce_iv_dec = ce_iv_pct / 100 if (ce_iv_pct is not None and ce_iv_pct > 0) else None
        ce_greeks = (
            _greeks("c", item_spot, strike, tte, ce_iv_dec)
            if (ce_iv_dec and item_spot > 0 and ce_ltp and ce_ltp > 0)
            else {"delta": None, "gamma": None, "theta": None, "vega": None, "rho": None}
        )

        rows.append({
            "expiry": expiry, "strike": strike, "option_type": "CE",
            "ltp": ce_ltp if ce_ltp is not None else 0.0,
            "volume": ce_vol, "oi": ce_oi, "oi_chg": ce_oi_chg,
            "iv": ce_iv_pct, "spot": item_spot, **ce_greeks,
        })

    df = pd.DataFrame(rows)
    logger.info("[SENSEX] Parsed %d rows for expiry %s (spot=%.2f)", len(df), expiry, spot or
                (_parse_float(raw_rows[0].get("UlaValue")) if raw_rows else 0))
    return df
