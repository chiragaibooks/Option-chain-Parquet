"""readme_generator.py — Auto-generates README.md with option chain tables."""
import logging
from datetime import datetime
from typing import Dict, Optional

import pandas as pd
import pytz

logger = logging.getLogger(__name__)
IST    = pytz.timezone("Asia/Kolkata")

_f  = lambda x: f"{x:.2f}" if pd.notna(x) and x is not None else "-"
_fi = lambda x: f"{int(x):,}" if pd.notna(x) and x is not None else "-"

_STRIKE_GAP = {"NIFTY50": 50, "BANKNIFTY": 100, "SENSEX": 100, "MIDCAPNIFTY": 25, "FINNIFTY": 50}


def _option_chain_table(symbol: str, df: pd.DataFrame, spot: float) -> str:
    if df.empty:
        return f"## 🔗 {symbol} Option Chain\n\n_No data available._\n\n"

    expiries = df["expiry"].unique()
    expiry   = expiries[0] if len(expiries) > 0 else ""
    df       = df[df["expiry"] == expiry].copy()

    ce  = df[df["option_type"] == "CE"].set_index("strike")
    pe  = df[df["option_type"] == "PE"].set_index("strike")
    gap = _STRIKE_GAP.get(symbol, 50)
    atm = round(spot / gap) * gap if spot else 0

    strikes = sorted(set(ce.index) | set(pe.index))

    header = (
        "<tr>"
        "<th>CE OI</th><th>CE Vol</th><th>CE IV</th><th>CE LTP</th><th>CE Δ</th>"
        "<th>Strike</th>"
        "<th>PE Δ</th><th>PE LTP</th><th>PE IV</th><th>PE Vol</th><th>PE OI</th>"
        "</tr>"
    )

    rows_html = ""
    for strike in strikes:
        is_atm = strike == atm
        style  = ' style="background:#fffde7;font-weight:bold;"' if is_atm else ""
        c = ce.loc[strike] if strike in ce.index else {}
        p = pe.loc[strike] if strike in pe.index else {}
        rows_html += (
            f"<tr{style}>"
            f"<td>{_fi(c.get('oi'))}</td><td>{_fi(c.get('volume'))}</td>"
            f"<td>{_f(c.get('iv'))}</td><td>{_f(c.get('ltp'))}</td><td>{_f(c.get('delta'))}</td>"
            f"<td><b>{int(strike)}</b>{'  ← ATM' if is_atm else ''}</td>"
            f"<td>{_f(p.get('delta'))}</td><td>{_f(p.get('ltp'))}</td>"
            f"<td>{_f(p.get('iv'))}</td><td>{_fi(p.get('volume'))}</td><td>{_fi(p.get('oi'))}</td>"
            f"</tr>\n"
        )

    return (
        f"## 🔗 {symbol} Option Chain &nbsp; `Expiry: {expiry}` &nbsp; `Spot: {spot:.2f}`\n\n"
        f"<table>\n{header}\n{rows_html}</table>\n\n"
    )


def update_readme(readme_path: str, option_data: Optional[Dict[str, tuple]] = None) -> None:
    ts      = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S IST")
    content = f"<!-- Auto-generated — {ts} -->\n\n**Last updated:** {ts}\n\n"

    if option_data:
        content += "# 📋 Option Chain\n\n"
        for sym, (df, spot) in option_data.items():
            content += _option_chain_table(sym, df, spot)
    else:
        content += "_No option chain data available._\n"

    try:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info("README updated: %s", readme_path)
    except OSError:
        logger.exception("Failed to write README: %s", readme_path)
