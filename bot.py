import requests
import time
import sqlite3
import json

database = sqlite3.connect('./botRecords.db')
dbMutation = database.cursor()

binanceAPI = "https://api.binance.com/api/v3/"
tickersBinance = []
tickersKraken = []

# Check if table exists
dbMutation.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='history' ''')
if dbMutation.fetchone()[0]==1:
    print('Table exists.')
else:
    dbMutation.execute('''CREATE TABLE history ([ID] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, [exchange] TEXT NOT NULL, [ticker] TEXT NOT NULL, [time] TEXT  NOT NULL, [dip] INTEGER)''')
    print("Table created")

# Read configuration
with open('configuration.json') as config:
    data = json.load(config)
    
    # Populate ticker arrays
    if (data["exchanges"]["binance"]["enabled"]):
     for i in range(len(data["exchanges"]["binance"]["tickers"])):
        tickersBinance.append(data["exchanges"]["binance"]["tickers"][i])
        
    if (data["exchanges"]["kraken"]["enabled"]):
     for i in range(len(data["exchanges"]["kraken"]["tickers"])):
        tickersKraken.append(data["exchanges"]["kraken"]["tickers"][i])
        
def storeIntoDB(exchange, ticker, time, dip):
    # Store stuff into table
    dbMutation.execute("INSERT INTO history VALUES ('" + exchange + "', '" + ticker + "', '" + time + "', '" + dip + "')")
    dbMutation.commit()
        
# Classes
class Binance:    
    # Acquire price    
    def getPrice(self, ticker):
        response = requests.get(binanceAPI + str("avgPrice?symbol=") + str(ticker))
        
        # Handle response
        if not response.status_code == 200:
            return "error acquiring price for " + str(ticker)
        else:
            return response.json()['price']

# Create instances of classes
binance = Binance()

# Acquire prices
for i in range(len(tickersBinance)):
    print(tickersBinance[i] + " " + binance.getPrice(tickersBinance[i]))