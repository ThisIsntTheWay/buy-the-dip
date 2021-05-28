import requests
import time
import sqlite3
import json

database = sqlite3.connect('./botRecords.db');
binanceAPI = "https://api.binance.com/api/v3/"
tickers = [""]

# Read configuration
with open('configuration.json') as config:
    data = json.load(config)
    
    # Populate tickers array
    for i in range(len(data["tickers"])):
        tickers.append(data["tickers"][i])

# loop to acquire ticker data
while True:
    time.sleep(5)
    
    # Iterate through prices
    for i in range(len(tickers)):
        response = requests.get(binanceAPI + str(tickers[i]))
        price = json.loads(response.content())
        
    # TODO: Save response in list
        
    # "avgPrice?symbol=BTCUSDT"