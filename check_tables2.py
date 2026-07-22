import sqlite3

conn = sqlite3.connect("data/option_chain.db")

print("=== SENSEX sample rows July 21 ===")
rows = conn.execute(
    "SELECT timestamp, strike, option_type, ltp, spot, iv, delta "
    "FROM sensex_option_chain WHERE timestamp LIKE '20260721%' LIMIT 15"
).fetchall()
for r in rows:
    print(r)

print()
print("=== SENSEX ltp > 0 count ===")
print(conn.execute("SELECT COUNT(*) FROM sensex_option_chain WHERE timestamp LIKE '20260721%' AND ltp > 0").fetchone()[0])

print()
print("=== SENSEX spot values ===")
rows2 = conn.execute(
    "SELECT DISTINCT spot FROM sensex_option_chain WHERE timestamp LIKE '20260721%'"
).fetchall()
for r in rows2:
    print(r)

print()
print("=== All tables: latest timestamp across all days ===")
for t in ["nifty50_option_chain","banknifty_option_chain","finnifty_option_chain","midcapnifty_option_chain","sensex_option_chain"]:
    r = conn.execute(f"SELECT MAX(timestamp) FROM {t}").fetchone()[0]
    print(f"  {t:<35} latest={r}")

conn.close()
