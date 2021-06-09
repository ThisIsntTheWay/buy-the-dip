# Database module

import sqlite3

database = sqlite3.connect('./botRecords.db')
dbMutation = database.cursor()

def storeIntoDB(exchange, ticker, time, dip, timeframe, note):
    # Store stuff into table
    dbMutation.execute("INSERT INTO history VALUES ('" + exchange + "', '" + ticker + "', '" + time + "', '" + dip + "', '" + timeframe + "', '" + note + "')")
    dbMutation.commit()
    
# Check if table exists
dbMutation.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='history' ''')
if dbMutation.fetchone()[0]==1:
    print('[INIT] Table exists.')
else:
    dbMutation.execute('''CREATE TABLE history ([ID] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, [exchange] TEXT NOT NULL, [ticker] TEXT NOT NULL, [time] TEXT NOT NULL, [timeframe] INTEGER, [dip] INTEGER, [result] TEXT)''')
    print('[INIT] Table created.')