# Binance module

import asyncio
import hmac
import hashlib
import requests
import time
import traceback

import modules.utils as utils
import modules.database as modDB
import modules.configuration as modConfig
import modules.discordBot as modBot

binanceAPI = "https://api.binance.com/api/v3/"

# ------------------------------
#  Async functions

async def binanceMonitor():
    await asyncio.sleep(8)
    if modConfig.canRun:
        while True:
            await asyncio.sleep(3)
            utils.log("[PRIC] Querying binance...")
            
            for i in range(len(modConfig.tickersBinance)):
                try:
                    priceNow = int(float(binance.getPrice(modConfig.tickersBinance[i])))

                    # Check if the price is below the dip threshold
                    # formula to calculate percentage change: 100 * (NEW_PRICE - OLD_RPICE) / OLD_PRICE
                    for base in modConfig.timeframePrice:
                        if base.exchange == "Binance" and base.ticker == modConfig.tickersBinance[i]:
                            percentage = 100 * (priceNow - base.price) / base.price
                            utils.log("   > " + modConfig.tickersBinance[i] + ": " + str(priceNow) + " - change: " + str(round(percentage, 2)) + "%")
                            
                            # Buy if the price has dipped below threshold and nothing has been bought before
                            if percentage < modConfig.dipThreshold and not base.bought:
                                utils.log("       > Percentage below threshold, buying!")
                                base.bought = True
                                
                                # Notify discord
                                msg = "Attempting to buy **" + base.ticker + "** at a price of **" + str(priceNow) + "** *(" + str(int(percentage))+ "%)* on **" + base.exchange + "**..."
                                await modBot.sendMsgByProxy(msg)
                                
                                # Attempt to buy and otify discord and console about result
                                msg, status = binance.buy(base.ticker)
                                
                                utils.log(msg)
                                await modBot.sendMsgByProxy("> `" + msg + "` @here")
                                modDB.storeIntoDB("binance", base.ticker, utils.getTime(), modConfig.timeframeNum, percentage, msg)
                except Exception as e:
                    utils.log("[X] An error occurred within binanceMonitor().")
                    traceback.print_exc()
                    
                    if modConfig.verbosity == 1:
                        msg = traceback.format_exception()
                    else:
                        msg = str(e)
                        
                    await modBot.sendMsgByProxy("\u274C Exception in binance subroutine: \n`" + str(msg) + "` @here")
                
# ------------------------------
#  Functions

def hash(query_string, secret):
    return hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
                    
# ------------------------------
#  Classes

class Binance:    
    # Acquire price
    def getPrice(self, ticker):
        response = requests.get(binanceAPI + str("ticker/price?symbol=") + str(ticker))
        
        # Handle response
        if response.status_code == 200:
            return response.json()['price']
        else:
            return utils.getTime() + "ERROR: " + str(response.status_code)
    
    def buy(self, ticker):
        # Assemble parameter string
        stake = modConfig.data["exchanges"]["binance"]["stake"]
        if stake < 1:
            return "\u274C Stake is less than 1! (Current: " + str(stake) + ")", False
        
        paramString = "symbol=" + str(ticker) + "&side=BUY&type=MARKET&quoteOrderQty=" + str(stake) + "&timestamp=" + str(int(time.time() * 1000))
        paramString = paramString + "&signature=" + str(hash(paramString, modConfig.data["exchanges"]["binance"]["api_secret"]))
        
        fullRequest = binanceAPI + "order?" + paramString
        #print(utils.getTime() + " [INFO] " + fullRequest)
        
        # Send POST
        headers = {'X-MBX-APIKEY': modConfig.data["exchanges"]["binance"]["api_key"]}
        response = requests.post(fullRequest.encode(), headers=headers)
        
        # Handle response
        if response.status_code == 200:        
            return "\u2705 [" + str(response.status_code) + "] " + str(response.json()), True
        else:
            return "\u274C [" + str(response.status_code) + "] " + str(response.json()), False           

# Create instances
binance = Binance()