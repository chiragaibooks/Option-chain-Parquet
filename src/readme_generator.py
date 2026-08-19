"""readme_generator.py — Writes README with latest parquet snapshot data."""
import glob
import logging
import os
from datetime import datetime

import pandas as pd
import pytz

logger = logging.getLogger(__name__)
IST = pytz.timezone("Asia/Kolkata")

_PARQUET_DIR = "data"
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
        return datetime.strptime(str(ts), "%Y%m%d%H%M").strftime("%d %b %Y %H:%M IST")
    except Exception:
        return str(ts)


def generate(parquet_dir: str = _PARQUET_DIR, out: str = _OUT) -> None:
    files = sorted(glob.glob(os.path.join(parquet_dir, "option_chain_*.parquet")), reverse=True)
    if not files:
        _write(out, "# 📋 NIFTY50 Option Chain\n\n_No parquet data yet._\n")
        return

    now_str = datetime.now(IST).strftime("%d %b %Y %H:%M:%S IST")
    content = f"<!-- auto-updated: {now_str} -->\n\n"
    content += "# 📋 NIFTY50 Option Chain — Parquet Data\n\n"
    content += f"**Updated:** {now_str}\n\n---\n\n"
    content += "🔍 **[Open Interactive Dashboard →](https://chiragaibooks.github.io/Option-chain-Parquet/)** — filter by Expiry, Strike, Type, LTP, view Greeks & OI charts\n\n---\n\n"

    # Last 10 snapshots from the most recent parquet file
    try:
        latest_file = files[0]
        df_latest = pd.read_parquet(latest_file)
        latest_timestamps = (
            df_latest["timestamp"].drop_duplicates().sort_values().tail(10).tolist()
        )

        content += f"## 🕐 Last 10 Snapshots — `{os.path.basename(latest_file)}`\n\n"

        for ts in reversed(latest_timestamps):
            rows = df_latest[df_latest["timestamp"] == ts][
                ["strike", "option_type", "expiry", "ltp"]
            ].sort_values(["strike", "option_type"]).values.tolist()

            content += f"### {_fmt_ts(ts)}\n\n"
            content += "<table>\n"
            content += "<tr><th>Expiry</th><th>Strike</th><th>Type</th><th>LTP</th></tr>\n"
            for strike, otype, expiry, ltp in rows:
                content += (
                    f"<tr><td>{expiry or '-'}</td><td>{int(strike)}</td>"
                    f"<td>{otype}</td><td>{_fmt(ltp)}</td></tr>\n"
                )
            content += "</table>\n\n---\n\n"
    except Exception:
        logger.exception("Failed to build snapshot section")

    _write(out, content)
    logger.info("README updated from parquet files: %d files", len(files))


def _write(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    generate()
