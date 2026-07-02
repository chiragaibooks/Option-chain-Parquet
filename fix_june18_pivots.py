"""
fix_june18_pivots.py — Seed June 18 pivots for symbols missing previous day data.
Run once: python fix_june18_pivots.py
"""
import sqlite3
import yfinance as yf

DB = "data/market_data.db"

# Symbols missing June 18 pivots and their yfinance tickers
SYMBOLS = {
    "NIFTY50":   "^NSEI",
    "BANKNIFTY": "^NSEBANK",
    "SENSEX":    "^BSESN",
}

conn = sqlite3.connect(DB)

for symbol, ticker in SYMBOLS.items():
    # Fetch June 17 daily OHLC from yfinance
    df = yf.download(ticker, start="2026-06-17", end="2026-06-18", interval="1d",
                     progress=False, auto_adjust=True)
    if df.empty:
        print(f"{symbol}: could not fetch June 17 data from yfinance")
        continue

    # Flatten MultiIndex columns if present
    if hasattr(df.columns, 'levels'):
        df.columns = [c[0].lower() for c in df.columns]
    else:
        df.columns = [c.lower() for c in df.columns]

    ph = float(df["high"].iloc[0])
    pl = float(df["low"].iloc[0])
    pc = float(df["close"].iloc[0])

    pivot    = (ph + pl + pc) / 3
    pivot_r1 = 2 * pivot - pl
    pivot_r2 = pivot + (ph - pl)
    pivot_r3 = ph + 2 * (pivot - pl)
    pivot_s1 = 2 * pivot - ph
    pivot_s2 = pivot - (ph - pl)
    pivot_s3 = pl - 2 * (ph - pivot)

    conn.execute("""
        UPDATE indexes SET
            pivot=?, pivot_r1=?, pivot_r2=?, pivot_r3=?,
            pivot_s1=?, pivot_s2=?, pivot_s3=?
        WHERE stock_name=? AND substr(datetime,1,10)='2026-06-18'
    """, (pivot, pivot_r1, pivot_r2, pivot_r3,
          pivot_s1, pivot_s2, pivot_s3, symbol))

    updated = conn.execute("SELECT changes()").fetchone()[0]
    print(f"{symbol}: June 17 H={ph} L={pl} C={pc} -> pivot={pivot:.2f} | updated {updated} rows")

conn.commit()
conn.close()
print("\nDone.")
