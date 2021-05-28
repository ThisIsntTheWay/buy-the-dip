import requests
import time
import sqlite3
import json

database = sqlite3.connect('./botRecords.db');
binanceAPI = "https://api.binance.com/api/v3/"
tickersBinance = []
tickersKraken = []

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

print(tickersBinance)
print(tickersKraken)