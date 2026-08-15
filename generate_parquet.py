"""
generate_parquet.py
Generates synthetic per-minute option chain parquet files for each
Mon–Fri trading day from 2025-08-18 to 2025-08-22 (9:15–15:30 IST).
Output: data/option_chain_YYYYMMDD.parquet
"""
import math
import random
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd
import pytz

IST = pytz.timezone("Asia/Kolkata")

# ── Config ────────────────────────────────────────────────────────────────────
START_DATE = date(2025, 8, 18)   # Monday
END_DATE   = date(2025, 8, 22)   # Friday
SPOT_BASE  = 24500.0
STRIKES    = list(range(23500, 25600, 100))   # 21 strikes
EXPIRY     = "21-Aug-2025"
SYMBOL     = "NIFTY50"
RISK_FREE  = 0.065
OUTPUT_DIR = "data"

COLS = [
    "timestamp", "symbol", "expiry", "strike", "option_type",
    "spot", "ltp", "open", "high", "low", "close",
    "volume", "oi", "oi_chg", "iv",
    "delta", "gamma", "theta", "vega", "rho",
]


# ── Helpers ───────────────────────────────────────────────────────────────────
def _d1_d2(S, K, t, iv):
    d1 = (math.log(S / K) + (RISK_FREE + 0.5 * iv ** 2) * t) / (iv * math.sqrt(t))
    return d1, d1 - iv * math.sqrt(t)


def _norm_cdf(x):
    from scipy.stats import norm
    return norm.cdf(x)


def _norm_pdf(x):
    from scipy.stats import norm
    return norm.pdf(x)


def _greeks(flag, S, K, t, iv):
    if not (S > 0 and K > 0 and t > 0 and iv > 0):
        return dict(delta=None, gamma=None, theta=None, vega=None, rho=None)
    try:
        d1, d2 = _d1_d2(S, K, t, iv)
        pdf_d1 = _norm_pdf(d1)
        gamma  = round(pdf_d1 / (S * iv * math.sqrt(t)), 6)
        vega   = round(S * pdf_d1 * math.sqrt(t) / 100, 4)
        if flag == "c":
            delta = round(_norm_cdf(d1), 4)
            theta = round((-S * pdf_d1 * iv / (2 * math.sqrt(t)) - RISK_FREE * K * math.exp(-RISK_FREE * t) * _norm_cdf(d2)) / 365, 4)
            rho   = round(K * t * math.exp(-RISK_FREE * t) * _norm_cdf(d2) / 100, 4)
        else:
            delta = round(_norm_cdf(d1) - 1, 4)
            theta = round((-S * pdf_d1 * iv / (2 * math.sqrt(t)) + RISK_FREE * K * math.exp(-RISK_FREE * t) * _norm_cdf(-d2)) / 365, 4)
            rho   = round(-K * t * math.exp(-RISK_FREE * t) * _norm_cdf(-d2) / 100, 4)
        return dict(delta=delta, gamma=gamma, theta=theta, vega=vega, rho=rho)
    except Exception:
        return dict(delta=None, gamma=None, theta=None, vega=None, rho=None)


def _bs_price(flag, S, K, t, iv):
    d1, d2 = _d1_d2(S, K, t, iv)
    if flag == "c":
        return S * _norm_cdf(d1) - K * math.exp(-RISK_FREE * t) * _norm_cdf(d2)
    return K * math.exp(-RISK_FREE * t) * _norm_cdf(-d2) - S * _norm_cdf(-d1)


def _minutes(day: date):
    """All 1-min timestamps from 9:15 to 15:30 IST."""
    start = IST.localize(datetime(day.year, day.month, day.day, 9, 15))
    end   = IST.localize(datetime(day.year, day.month, day.day, 15, 30))
    ts = []
    cur = start
    while cur <= end:
        ts.append(cur)
        cur += timedelta(minutes=1)
    return ts


def _spot_series(n: int, base: float) -> list:
    """Random walk spot prices."""
    rng = np.random.default_rng(seed=int(base))
    returns = rng.normal(0, 0.0003, n)
    prices = base * np.cumprod(1 + returns)
    return prices.tolist()


# ── Main ──────────────────────────────────────────────────────────────────────
def generate_day(day: date) -> pd.DataFrame:
    timestamps = _minutes(day)
    spots = _spot_series(len(timestamps), SPOT_BASE + random.uniform(-200, 200))

    expiry_date = datetime.strptime(EXPIRY, "%d-%b-%Y").date()
    rows = []

    for i, (ts, spot) in enumerate(zip(timestamps, spots)):
        ts_str = ts.strftime("%Y%m%d%H%M")
        tte = max((expiry_date - day).days, 0.5) / 365.0

        for strike in STRIKES:
            for otype, flag in (("CE", "c"), ("PE", "p")):
                iv = round(random.uniform(0.10, 0.30), 4)
                ltp = round(max(_bs_price(flag, spot, strike, tte, iv), 0.05), 2)
                # Simulate OHLC around ltp
                spread = ltp * 0.01
                open_  = round(ltp + random.uniform(-spread, spread), 2)
                high_  = round(max(ltp, open_) + random.uniform(0, spread), 2)
                low_   = round(min(ltp, open_) - random.uniform(0, spread), 2)
                close_ = ltp
                vol    = random.randint(100, 5000)
                oi     = random.randint(1000, 100000)
                oi_chg = random.randint(-500, 500)
                g = _greeks(flag, spot, strike, tte, iv)
                rows.append({
                    "timestamp":   ts_str,
                    "symbol":      SYMBOL,
                    "expiry":      EXPIRY,
                    "strike":      float(strike),
                    "option_type": otype,
                    "spot":        round(spot, 2),
                    "ltp":         ltp,
                    "open":        open_,
                    "high":        high_,
                    "low":         low_,
                    "close":       close_,
                    "volume":      float(vol),
                    "oi":          float(oi),
                    "oi_chg":      float(oi_chg),
                    "iv":          round(iv * 100, 2),
                    **g,
                })

    return pd.DataFrame(rows, columns=COLS)


def main():
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cur = START_DATE
    while cur <= END_DATE:
        if cur.weekday() < 5:   # Mon–Fri only
            df = generate_day(cur)
            path = os.path.join(OUTPUT_DIR, f"option_chain_{cur.strftime('%Y%m%d')}.parquet")
            df.to_parquet(path, index=False)
            print(f"Created {path}  ({len(df):,} rows)")
        cur += timedelta(days=1)


if __name__ == "__main__":
    main()
