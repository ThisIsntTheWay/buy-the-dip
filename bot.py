import requests
import time
import json

binanceAPI = "https://api.binance.com/api/v3/"
tickers = [""]

# Read configuration
with open('configuration.json') as config:
    data = json.load(config)
    
    # Populate tickers array
    for i in range(len(data["tickers"])):
        tickers.append(data["tickers"][i])

# Create price class
class Prices:
    def __init__(asset, price, last, time):
        self.asset = asset
        self.price = price
        self.last = last
        self.time = time

# loop to acquire ticker data
while True:
    time.sleep(5)
    
    prices = []
    for i in range(len(tickers)):
        
    # "avgPrice?symbol=BTCUSDT"