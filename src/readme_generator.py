"""readme_generator.py — Writes README with last 10 NIFTY50 option chain snapshots."""
import sqlite3
import logging
from datetime import datetime

import pytz

logger = logging.getLogger(__name__)
IST = pytz.timezone("Asia/Kolkata")

_DB  = "data/option_chain.db"
_OUT = "README.md"
_GAP = 50


def _fmt(v):
    if v is None:
        return "-"
    try:
        return f"{float(v):,.2f}"
    except Exception:
        return "-"


def _fmt_ts(ts: str) -> str:
    try:
        return datetime.strptime(ts, "%Y%m%d%H%M").strftime("%d %b %Y %H:%M IST")
    except Exception:
        return ts


def _atm(spot: float) -> int:
    return round(spot / _GAP) * _GAP


def generate(db: str = _DB, out: str = _OUT) -> None:
    try:
        with sqlite3.connect(db) as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS nifty50_option_chain ("
                "timestamp TEXT, symbol TEXT, expiry TEXT, strike REAL, option_type TEXT,"
                "spot REAL, ltp REAL, open REAL, high REAL, low REAL, close REAL,"
                "volume REAL, oi REAL, oi_chg REAL, iv REAL,"
                "delta REAL, gamma REAL, theta REAL, vega REAL, rho REAL,"
                "PRIMARY KEY (timestamp, strike, option_type, expiry))"
            )
            ts_rows = conn.execute(
                "SELECT DISTINCT timestamp FROM nifty50_option_chain "
                "ORDER BY timestamp DESC LIMIT 10"
            ).fetchall()
    except Exception:
        logger.exception("Failed to read DB")
        return

    if not ts_rows:
        _write(out, "# 📋 NIFTY50 Option Chain\n\n_No data yet._\n")
        return

    timestamps = [r[0] for r in ts_rows]
    now_str    = datetime.now(IST).strftime("%d %b %Y %H:%M:%S IST")
    content    = f"<!-- auto-updated: {now_str} -->\n\n"
    content   += "# 📋 NIFTY50 Option Chain — Last 10 Snapshots\n\n"
    content   += f"**Updated:** {now_str}\n\n---\n\n"

    for ts in timestamps:
        try:
            with sqlite3.connect(db) as conn:
                rows = conn.execute(
                    "SELECT strike, option_type, spot, ltp, oi, oi_chg, volume, iv, delta "
                    "FROM nifty50_option_chain WHERE timestamp=? ORDER BY strike",
                    (ts,)
                ).fetchall()
        except Exception:
            continue

        if not rows:
            continue

        spot    = next((r[2] for r in rows if r[2]), 0.0)
        atm     = _atm(spot) if spot else 0
        ce      = {r[0]: r for r in rows if r[1] == "CE"}
        pe      = {r[0]: r for r in rows if r[1] == "PE"}
        strikes = sorted(set(ce) | set(pe))

        content += f"## 🕐 {_fmt_ts(ts)} &nbsp;|&nbsp; Spot: **{_fmt(spot)}** &nbsp;|&nbsp; ATM: **{atm}**\n\n"
        content += "<table>\n"
        content += "<tr><th>CE OI</th><th>CE Vol</th><th>CE IV</th><th>CE LTP</th><th>CE Δ</th>"
        content += "<th>Strike</th>"
        content += "<th>PE Δ</th><th>PE LTP</th><th>PE IV</th><th>PE Vol</th><th>PE OI</th></tr>\n"

        for strike in strikes:
            c      = ce.get(strike, [None]*9)
            p      = pe.get(strike, [None]*9)
            is_atm = strike == atm
            style  = ' style="background:#fffde7;font-weight:bold;"' if is_atm else ""
            atm_tag = " ← ATM" if is_atm else ""
            content += (
                f"<tr{style}>"
                f"<td>{_fmt(c[4])}</td><td>{_fmt(c[6])}</td><td>{_fmt(c[7])}</td>"
                f"<td>{_fmt(c[3])}</td><td>{_fmt(c[8])}</td>"
                f"<td><b>{int(strike)}</b>{atm_tag}</td>"
                f"<td>{_fmt(p[8])}</td><td>{_fmt(p[3])}</td><td>{_fmt(p[7])}</td>"
                f"<td>{_fmt(p[6])}</td><td>{_fmt(p[4])}</td>"
                f"</tr>\n"
            )
        content += "</table>\n\n---\n\n"

    _write(out, content)
    logger.info("README updated with %d snapshots", len(timestamps))


def _write(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    generate()
