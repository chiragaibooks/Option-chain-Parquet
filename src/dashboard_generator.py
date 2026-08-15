"""dashboard_generator.py — Writes docs/data.json for the GitHub Pages dashboard."""
import json
import logging
import math
import os
import sqlite3
from datetime import datetime

import pytz

logger = logging.getLogger(__name__)
IST = pytz.timezone("Asia/Kolkata")

_DB  = "data/option_chain.db"
_OUT = "docs/data.json"


def _safe(v):
    if v is None:
        return None
    try:
        f = float(v)
        return None if math.isnan(f) or math.isinf(f) else round(f, 2)
    except Exception:
        return None


def generate(db: str = _DB, out: str = _OUT) -> None:
    os.makedirs(os.path.dirname(out), exist_ok=True)

    try:
        with sqlite3.connect(db) as conn:
            ts_rows = conn.execute(
                "SELECT DISTINCT timestamp FROM nifty50_option_chain "
                "ORDER BY timestamp DESC LIMIT 10"
            ).fetchall()
    except Exception:
        logger.exception("dashboard_generator: failed to read DB")
        _write(out, {"updated": _now_str(), "snapshots": []})
        return

    if not ts_rows:
        _write(out, {"updated": _now_str(), "snapshots": []})
        return

    snapshots = []
    for (ts,) in ts_rows:
        try:
            with sqlite3.connect(db) as conn:
                rows = conn.execute(
                    "SELECT strike, option_type, expiry, ltp, oi, oi_chg, "
                    "volume, iv, delta, gamma, theta, vega, rho, spot "
                    "FROM nifty50_option_chain WHERE timestamp=? "
                    "ORDER BY strike, option_type",
                    (ts,),
                ).fetchall()
        except Exception:
            continue

        if not rows:
            continue

        spot = _safe(rows[0][13]) if rows else None
        expiries = sorted({r[2] for r in rows if r[2]})

        chain: dict = {}
        for strike, otype, expiry, ltp, oi, oi_chg, vol, iv, delta, gamma, theta, vega, rho, _ in rows:
            key = f"{expiry}|{strike}"
            if key not in chain:
                chain[key] = {"strike": _safe(strike), "expiry": expiry, "CE": None, "PE": None}
            chain[key][otype] = {
                "ltp":    _safe(ltp),
                "oi":     _safe(oi),
                "oiChg":  _safe(oi_chg),
                "volume": _safe(vol),
                "iv":     _safe(iv),
                "delta":  _safe(delta),
                "gamma":  _safe(gamma),
                "theta":  _safe(theta),
                "vega":   _safe(vega),
                "rho":    _safe(rho),
            }

        snapshots.append({
            "timestamp": ts,
            "label": _fmt_ts(ts),
            "spot": spot,
            "expiries": expiries,
            "rows": sorted(chain.values(), key=lambda x: (x["expiry"], x["strike"])),
        })

    _write(out, {"updated": _now_str(), "snapshots": snapshots})
    logger.info("dashboard data.json written — %d snapshots", len(snapshots))


def _fmt_ts(ts: str) -> str:
    try:
        return datetime.strptime(ts, "%Y%m%d%H%M").strftime("%d %b %Y %H:%M IST")
    except Exception:
        return ts


def _now_str() -> str:
    return datetime.now(IST).strftime("%d %b %Y %H:%M:%S IST")


def _write(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"))


if __name__ == "__main__":
    generate()
