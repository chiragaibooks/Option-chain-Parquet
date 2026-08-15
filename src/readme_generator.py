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
        "<details open>\n"
        "<summary><b>🔍 Filters</b></summary>\n\n"
        "<p>\n"
        "<label><b>Expiry:</b></label> "
        '<select id=\'expiry-filter\' onchange=\'applyFilters()\'>'  
        '<option value=\'\'>All</option>' + expiry_options + '</select>\n'
        "&nbsp;&nbsp;"
        "<label><b>Type:</b></label> "
        "<label><input type='radio' name='type-filter' value='' checked onchange='applyFilters()'> All</label> "
        "<label><input type='radio' name='type-filter' value='CE' onchange='applyFilters()'> CE</label> "
        "<label><input type='radio' name='type-filter' value='PE' onchange='applyFilters()'> PE</label>\n"
        "</p>\n"
        "</details>\n\n"
        "<script>\n"
        "function applyFilters() {\n"
        "  var expiry = document.getElementById('expiry-filter').value;\n"
        "  var type = document.querySelector('input[name=type-filter]:checked').value;\n"
        "  document.querySelectorAll('table tr[data-expiry]').forEach(function(row) {\n"
        "    var eMatch = !expiry || row.dataset.expiry === expiry;\n"
        "    var tMatch = !type || row.dataset.type === type;\n"
        "    row.style.display = (eMatch && tMatch) ? '' : 'none';\n"
        "  });\n"
        "}\n"
        "</script>\n\n"
    )

    for ts, rows in snapshot_data:
        content += f"## 🕐 {_fmt_ts(ts)}\n\n"
        content += "<table>\n"
        content += "<tr><th>Timestamp</th><th>Expiry</th><th>Strike</th><th>Type</th><th>LTP</th></tr>\n"

        for strike, otype, expiry, ltp in rows:
            content += (
                f"<tr data-expiry='{expiry or ''}' data-type='{otype}'>"
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
