import sqlite3, pandas as pd

conn = sqlite3.connect('data/option_chain.db')
tables = ['nifty50_option_chain', 'banknifty_option_chain', 'midcapnifty_option_chain', 'finnifty_option_chain']

for table in tables:
    df = pd.read_sql(f'SELECT * FROM {table}', conn)
    df.to_csv(f'data/{table}.csv', index=False)
    print(f'{table}: {len(df)} rows exported')

conn.close()
