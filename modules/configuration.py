# Configuration module

import sys
import json

import modules.utils as utils

# This file parses the json configuration
allTickers = []

# Unified ticker[]
# a = [["binance", ["ETHUSDT", "BTCUSDT"]], ["kraken", ["ETHCHF", "BTCCHF"]]]

# Read configuration
with open('configuration.json') as config:
    data = json.load(config)
    
    # Populate ticker arrays
    # Binance
    if (data["exchanges"]["binance"]["enabled"]):
        allTickers.append(["binance"])
        allTickers[0].append(data["exchanges"]["binance"]["tickers"])
    
    # Kraken
    if (data["exchanges"]["kraken"]["enabled"]):
        allTickers.append(["kraken"])
        
        # Determine the correct index of allTickers
        if allTickers[0][0] == "binance":
            allTickers[1].append(data["exchanges"]["kraken"]["tickers"])
        else:
            allTickers[0].append(data["exchanges"]["kraken"]["tickers"])
    
    # Coinbase
    if (data["exchanges"]["coinbase"]["enabled"]):
        allTickers.append(["coinbase"])
        
        # Determine the correct index of allTickers
        if allTickers[0][0] == "binance":
            if allTickers[1][0] == "kraken":
                allTickers[2].append(data["exchanges"]["coinbase"]["tickers"])
            else:
                allTickers[1].append(data["exchanges"]["coinbase"]["tickers"])
        else:
            allTickers[0].append(data["exchanges"]["kraken"]["tickers"])
        
    # Read misc config
    timeframe = data["dip_config"]["timeframe"]
    
    dipMode = data["dip_config"]["mode"]
    if dipMode == "threshold":
        #dipThreshold = data["dip_config"]["threshold"]
        #dipThreshold = -dipThreshold
        dipThreshold = 5
    elif dipMode == "tiered":
        dipTiers = []
        for i in range(len(data["dip_config"]["tiers"])):
            dipTiers.append(data["dip_config"]["tiers"][i])
            
        utils.log("[X] dipMode \"" + dipMode + "\" not yet implemented!")
        sys.exit()
    elif dipMode == "interval":
        dipInterval = ["dip_config"]["interval"]
        
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