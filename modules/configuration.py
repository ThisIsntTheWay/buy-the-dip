# Configuration module

import json

# This file parses the json configuration
tickersBinance = []
tickersKraken = []
tickersCoinbase = []
timeframePrice = []

# Read configuration
with open('configuration.json') as config:
    data = json.load(config)
    
    # Populate ticker arrays
    # Binance
    if (data["exchanges"]["binance"]["enabled"]):
        for i in range(len(data["exchanges"]["binance"]["tickers"])):
            tickersBinance.append(data["exchanges"]["binance"]["tickers"][i])
    
    # Kraken
    if (data["exchanges"]["kraken"]["enabled"]):
        for i in range(len(data["exchanges"]["kraken"]["tickers"])):
            tickersKraken.append(data["exchanges"]["kraken"]["tickers"][i])
        
    # Read misc config
    timeframe = data["dip_config"]["timeframe"]
    #dipThreshold = data["dip_config"]["threshold"]
    #dipThreshold = -dipThreshold
    dipThreshold = 5
    
# Object to use as a base price for all intervals
class basePrice:
    def __init__(self, exchange, ticker, price, bought):
        self.exchange = exchange
        self.ticker = ticker
        self.price = price
        self.bought = bought