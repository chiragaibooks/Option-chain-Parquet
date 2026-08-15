"""readme_generator.py — Writes README with last 10 NIFTY50 option chain snapshots."""
import sqlite3
import logging
from datetime import datetime

import pytz

logger = logging.getLogger(__name__)
IST = pytz.timezone("Asia/Kolkata")

_DB  = "data/option_chain.db"
_OUT = "README.md"


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


def generate(db: str = _DB, out: str = _OUT) -> None:
    try:
        with sqlite3.connect(db) as conn:
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

    # Collect all expiries for filter dropdown
    all_expiries: set = set()
    snapshot_data = []
    for ts in timestamps:
        try:
            with sqlite3.connect(db) as conn:
                rows = conn.execute(
                    "SELECT strike, option_type, expiry, ltp "
                    "FROM nifty50_option_chain WHERE timestamp=? ORDER BY strike, option_type",
                    (ts,)
                ).fetchall()
        except Exception:
            continue
        if not rows:
            continue
        for _, _, expiry, _ in rows:
            if expiry:
                all_expiries.add(expiry)
        snapshot_data.append((ts, rows))

    # Filter UI (JS — works in browsers; GitHub ignores scripts)
    expiry_options = "".join(
        f'<option value="{e}">{e}</option>' for e in sorted(all_expiries)
    )
    content += (
        "<script>\n"
        "function applyFilters() {\n"
        "  var expiry = document.getElementById('f-expiry').value;\n"
        "  var type   = document.getElementById('f-type').value;\n"
        "  var sMin   = parseFloat(document.getElementById('f-strike-min').value) || -Infinity;\n"
        "  var sMax   = parseFloat(document.getElementById('f-strike-max').value) || Infinity;\n"
        "  var lMin   = parseFloat(document.getElementById('f-ltp-min').value)    || -Infinity;\n"
        "  var lMax   = parseFloat(document.getElementById('f-ltp-max').value)    || Infinity;\n"
        "  document.querySelectorAll('table tr[data-expiry]').forEach(function(row) {\n"
        "    var eMatch = !expiry || row.dataset.expiry === expiry;\n"
        "    var tMatch = !type   || row.dataset.type   === type;\n"
        "    var strike = parseFloat(row.dataset.strike);\n"
        "    var ltp    = parseFloat(row.dataset.ltp);\n"
        "    var sMatch = strike >= sMin && strike <= sMax;\n"
        "    var lMatch = ltp    >= lMin && ltp    <= lMax;\n"
        "    row.style.display = (eMatch && tMatch && sMatch && lMatch) ? '' : 'none';\n"
        "  });\n"
        "}\n"
        "function resetFilters() {\n"
        "  ['f-expiry','f-type','f-strike-min','f-strike-max','f-ltp-min','f-ltp-max'].forEach(function(id){\n"
        "    document.getElementById(id).value='';\n"
        "  });\n"
        "  applyFilters();\n"
        "}\n"
        "</script>\n\n"
        "<details open>\n"
        "<summary><b>🔍 Column Filters</b></summary>\n\n"
        "<table>\n"
        "<tr>\n"
        "  <th>Expiry</th>\n"
        "  <th>Strike Min</th><th>Strike Max</th>\n"
        "  <th>Type</th>\n"
        "  <th>LTP Min</th><th>LTP Max</th>\n"
        "  <th></th>\n"
        "</tr>\n"
        "<tr>\n"
        f"  <td><select id='f-expiry' onchange='applyFilters()'><option value=''>All</option>{expiry_options}</select></td>\n"
        "  <td><input id='f-strike-min' type='number' placeholder='e.g. 24000' oninput='applyFilters()' style='width:90px'></td>\n"
        "  <td><input id='f-strike-max' type='number' placeholder='e.g. 25000' oninput='applyFilters()' style='width:90px'></td>\n"
        "  <td><select id='f-type' onchange='applyFilters()'><option value=''>All</option><option>CE</option><option>PE</option></select></td>\n"
        "  <td><input id='f-ltp-min' type='number' placeholder='e.g. 10' oninput='applyFilters()' style='width:80px'></td>\n"
        "  <td><input id='f-ltp-max' type='number' placeholder='e.g. 500' oninput='applyFilters()' style='width:80px'></td>\n"
        "  <td><button onclick='resetFilters()'>Reset</button></td>\n"
        "</tr>\n"
        "</table>\n\n"
        "</details>\n\n"
    )

    for ts, rows in snapshot_data:
        content += f"## 🕐 {_fmt_ts(ts)}\n\n"
        content += "<table>\n"
        content += "<tr><th>Timestamp</th><th>Expiry</th><th>Strike</th><th>Type</th><th>LTP</th></tr>\n"

        for strike, otype, expiry, ltp in rows:
            ltp_raw = float(ltp) if ltp is not None else 0
            content += (
                f"<tr data-expiry='{expiry or ''}' data-type='{otype}' "
                f"data-strike='{int(strike)}' data-ltp='{ltp_raw}'>"
                f"<td>{_fmt_ts(ts)}</td>"
                f"<td>{expiry or '-'}</td>"
                f"<td>{int(strike)}</td>"
                f"<td>{otype}</td>"
                f"<td>{_fmt(ltp)}</td>"
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
