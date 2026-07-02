import sqlite3, pandas as pd
conn = sqlite3.connect('data/market_data.db')
pd.read_sql('SELECT * FROM indexes', conn).to_csv('data/market_data.csv', index=False)
conn.close()
print('Exported successfully')
