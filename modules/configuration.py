# Configuration module
# This file parses the json configuration

import sys
import json

import modules.utils as utils

tickersBinance = []
tickersKraken = []
tickersCoinbase = []
timeframePrice = []
timeframeStart = 0

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
    
    dipMode = data["dip_config"]["mode"]
    if dipMode == "threshold":
        dipThreshold = data["dip_config"]["threshold"]
        dipThreshold = -dipThreshold
        #dipThreshold = 5
    elif dipMode == "tiered":
        dipTiers = []
        for i in range(len(data["dip_config"]["tiers"])):
            dipTiers.append(data["dip_config"]["tiers"][i])
            
        utils.log("[X] dipMode \"" + dipMode + "\" not yet implemented!")
        sys.exit()
    elif dipMode == "interval":
        dipInterval = data["dip_config"]["interval"]
        
        utils.log("[X] dipMode \"" + dipMode + "\" not yet implemented!")
        sys.exit()
    else:
        utils.log("[X] dipMode \"" + dipMode + "\" is not known!")
        sys.exit()
    
# Object to use as a base price for all intervals
class basePrice:
    def __init__(self, exchange, ticker, price, bought, timesBought):
        self.exchange = exchange
        self.ticker = ticker
        self.price = price
        self.bought = bought
        self.timesBought = timesBought