import sqlite3
import pandas as pd

DB = "data/market_data.db"

conn = sqlite3.connect(DB)
df = pd.read_sql("SELECT stock_name, datetime, high, low, close FROM indexes ORDER BY stock_name, datetime", conn)
print(f"Loaded {len(df)} rows")

df["_date"] = df["datetime"].str[:10]
total_updated = 0

for sym, sym_df in df.groupby("stock_name"):
    daily = (
        sym_df.groupby("_date")
        .agg(d_high=("high", "max"), d_low=("low", "min"), d_close=("close", "last"))
        .reset_index()
        .sort_values("_date")
    )
    daily["ph"] = daily["d_high"].shift(1)
    daily["pl"] = daily["d_low"].shift(1)
    daily["pc"] = daily["d_close"].shift(1)
    daily = daily.dropna(subset=["ph"])

    daily["pivot"]    = (daily["ph"] + daily["pl"] + daily["pc"]) / 3
    daily["pivot_r1"] = 2 * daily["pivot"] - daily["pl"]
    daily["pivot_r2"] = daily["pivot"] + (daily["ph"] - daily["pl"])
    daily["pivot_r3"] = daily["ph"] + 2 * (daily["pivot"] - daily["pl"])
    daily["pivot_s1"] = 2 * daily["pivot"] - daily["ph"]
    daily["pivot_s2"] = daily["pivot"] - (daily["ph"] - daily["pl"])
    daily["pivot_s3"] = daily["pl"] - 2 * (daily["ph"] - daily["pivot"])

    rows_updated = 0
    for _, row in daily.iterrows():
        conn.execute("""
            UPDATE indexes SET
                pivot=?, pivot_r1=?, pivot_r2=?, pivot_r3=?,
                pivot_s1=?, pivot_s2=?, pivot_s3=?
            WHERE stock_name=? AND substr(datetime,1,10)=?
        """, (
            row["pivot"], row["pivot_r1"], row["pivot_r2"], row["pivot_r3"],
            row["pivot_s1"], row["pivot_s2"], row["pivot_s3"],
            sym, row["_date"]
        ))
        rows_updated += conn.execute("SELECT changes()").fetchone()[0]

    print(f"  {sym}: {rows_updated} rows updated")
    total_updated += rows_updated

conn.commit()
conn.close()
print(f"\nTotal updated: {total_updated} rows")

# verify
conn = sqlite3.connect(DB)
rows = conn.execute("""
    SELECT stock_name,
           SUM(CASE WHEN pivot IS NULL THEN 1 ELSE 0 END) AS null_pivots,
           SUM(CASE WHEN pivot IS NOT NULL THEN 1 ELSE 0 END) AS filled
    FROM indexes GROUP BY stock_name
""").fetchall()
conn.close()
print("\nFinal status:")
for r in rows:
    print(f"  {r[0]}: filled={r[2]}, null={r[1]}")
