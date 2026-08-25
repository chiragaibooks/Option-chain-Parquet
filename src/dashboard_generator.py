"""dashboard_generator.py — Writes docs/data.json for the GitHub Pages dashboard."""
import json
import logging
import math
import os
from datetime import datetime

import pandas as pd
import pytz

logger = logging.getLogger(__name__)
IST = pytz.timezone("Asia/Kolkata")

_OUT = "docs/data.json"
_SNAPSHOTS = 10  # most recent timestamps to include


def _safe(v):
    if v is None:
        return None
    try:
        f = float(v)
        return None if math.isnan(f) or math.isinf(f) else round(f, 2)
    except Exception:
        return None


def _load_recent_data() -> pd.DataFrame:
    """Load rows from the most recent available parquet files."""
    from src.database import list_available_dates, load_day

    dates = list_available_dates()
    if not dates:
        return pd.DataFrame()

    # Load from most recent dates until we have enough timestamps
    frames = []
    for d in reversed(dates):
        df = load_day(d)
        if not df.empty:
            frames.append(df)
        if frames:
            combined = pd.concat(frames, ignore_index=True)
            n_ts = combined["timestamp"].nunique() if "timestamp" in combined.columns else 0
            if n_ts >= _SNAPSHOTS:
                break
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def generate(out: str = _OUT) -> None:
    os.makedirs(os.path.dirname(out) if os.path.dirname(out) else ".", exist_ok=True)

    df = _load_recent_data()

    if df.empty or "timestamp" not in df.columns:
        _write(out, {"updated": _now_str(), "snapshots": []})
        return

    # Pick the most recent N distinct timestamps
    top_ts = sorted(df["timestamp"].unique(), reverse=True)[:_SNAPSHOTS]

    snapshots = []
    for ts in sorted(top_ts, reverse=True):
        rows_df = df[df["timestamp"] == ts]
        if rows_df.empty:
            continue

        spot = _safe(rows_df["spot"].iloc[0]) if "spot" in rows_df.columns else None
        expiries = sorted(rows_df["expiry"].dropna().unique().tolist())

        chain: dict = {}
        for _, r in rows_df.iterrows():
            key = f"{r.get('expiry')}|{r.get('strike')}"
            if key not in chain:
                chain[key] = {
                    "strike": _safe(r.get("strike")),
                    "expiry": r.get("expiry"),
                    "CE": None,
                    "PE": None,
                }
            otype = str(r.get("option_type", "")).upper()
            chain[key][otype] = {
                "ltp":    _safe(r.get("ltp")),
                "oi":     _safe(r.get("oi")),
                "oiChg":  _safe(r.get("oi_chg")),
                "volume": _safe(r.get("volume")),
                "iv":     _safe(r.get("iv")),
                "delta":  _safe(r.get("delta")),
                "gamma":  _safe(r.get("gamma")),
                "theta":  _safe(r.get("theta")),
                "vega":   _safe(r.get("vega")),
                "rho":    _safe(r.get("rho")),
            }

        snapshots.append({
            "timestamp": ts,
            "label":     _fmt_ts(ts),
            "spot":      spot,
            "expiries":  expiries,
            "rows":      sorted(chain.values(), key=lambda x: (x["expiry"], x["strike"])),
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
