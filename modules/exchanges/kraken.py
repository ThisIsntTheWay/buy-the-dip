# Kraken module

import asyncio
import hmac
import hashlib
from discord.ext.commands.errors import CheckAnyFailure
import requests
import time
import base64
import urllib.parse
import traceback

import modules.utils as utils
import modules.database as modDB
import modules.configuration as modConfig
import modules.discordBot as modBot

krakenAPI = "https://api.kraken.com"

# ------------------------------
#  Async functions

async def krakenMonitor():
    await asyncio.sleep(8)
    
    while True:
        await asyncio.sleep(3)

        if modConfig.canRun:
            utils.log("[PRIC] Querying kraken...")
            
            try:
                for i in range(len(modConfig.tickersKraken)):
                    modConfig.lastUpdate = int(time.time())
                    data, status = kraken.getPrice(modConfig.tickersKraken[i])
                    
                    if status:
                        priceNow = int(float(data))
                        
                        # Check if the price is below the dip threshold            
                        for base in modConfig.timeframePrice:
                            if base.exchange == "Kraken" and base.ticker == modConfig.tickersKraken[i]:
                                percentage = 100 * (priceNow - base.price) / base.price
                                utils.log("   > " + modConfig.tickersKraken[i] + ": " + str(priceNow) + " - change: " + str(round(percentage, 2)) + "%")
                                
                                # Buy if the price has dipped below threshold and nothing has been bought before
                                if percentage < modConfig.dipThreshold and not base.bought:
                                    utils.log("       > Percentage below threshold, buying!")
                                    base.bought = True
                                    
                                    msg = "Attempting to buy **" + base.ticker + "** at a price of **" + str(priceNow) + "** *(" + str(int(percentage))+ "%)* on **" + base.exchange + "**..."
                                    await modBot.sendMsgByProxy(msg)
                                    
                                    # Attempt to buy and otify discord and console about result
                                    msg, status = kraken.buy(base.ticker, priceNow)
                                    
                                    utils.log(msg)
                                    modDB.storeIntoDB("kraken", base.ticker, utils.getTime(), modConfig.timeframeNum, percentage, msg)
                                    
                                    await modBot.sendMsgByProxy("> `" + msg + "` @here")
                    else:
                        utils.log("   > Failed to get price: " + str(data))
                                                       
            except Exception as e:
                utils.log("[X] An error occurred within krakenMonitor()")
                traceback.print_exc()
                    
                if modConfig.verbosity == 1:
                    msg = str(traceback.format_exception())
                else:
                    msg = str(e)
                
                utils.log("[D] Attempting to inform discord...")
                try:
                    await modBot.sendMsgByProxy("\u274C Exception in kraken subroutine: \n`" + str(msg) + "` @here")
                except Exception as e:
                    utils.log("[X] Could not inform discord of exception: " + str(e))
                utils.log("[D] Done attempting.")

# ------------------------------
#  Functions

# Copied straight from the kraken API docs
def getSignature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = getSignature(uri_path, data, api_sec)             
    req = requests.post((krakenAPI + uri_path), headers=headers, data=data)
    return req

# ------------------------------
#  Classes

class Kraken:
    def getPrice(self, ticker):
        # Use request with fiddler: 'proxies={"http": "http://127.0.0.1:8888", "https":"http:127.0.0.1:8888"}, verify=r"FiddlerRoot.pem"'
        try:
            response = requests.get(krakenAPI + str("/0/public/Ticker?pair=") + str(ticker))

            # Handle response
            if response.status_code == 200:
                # Kraken is hipster and doesn't necessarily return a ticker we except (Eg: want BTCUSDT, get *XXBT*USD)
                # As such, we need to save all keys on the second level (after 'result') into a list and access the first index, which is the ticker we want.
                # It's stupid >:(
            
                rTicker = list(response.json()["result"].keys())[0]
                return response.json()['result'][rTicker]['c'][0], True
            else:
                return "HTTP/" + str(response.status_code) + " - " + str(response.text), False
        except Exception as e:
            utils.log("[kraken] GetPrice() has returned a fault: " + str(e))
            return 0
    
    def buy(self, ticker, priceNow):
        stake = modConfig.data["exchanges"]["kraken"]["stake"]
        if stake < 1:
            return "\u274C Stake is less than 1! (Current: " + str(stake) + ")", False
        
        #print("" + str(stake / priceNow))
        #print("volume: " + str(stake / priceNow) + " calculated using STAKE (" + str(stake) + ") and PRICENOW (" + str(priceNow) + ")")
        
        response = kraken_request('/0/private/AddOrder', {
            "nonce": str(int(1000*time.time())),
            "ordertype": "market",
            "type": "buy",
            "volume": str(stake / priceNow),
            "pair": ticker
        }, modConfig.data["exchanges"]["kraken"]["api_key"], modConfig.data["exchanges"]["kraken"]["api_secret"])

        # Handle response
        # > Because kraken is against standards, its API will NOT return HTTP/4xx on an error
        #   As such, we need to check if error[] is empty or not
        if len(response.json()['error']) == 0:
            return "\u2705 [" + str(response.status_code) + "] " + str(response.json()['result']), True
        else:
            return "\u274C [" + str(response.status_code) + "] " + str(response.json()), False

# Create instances
kraken = Kraken()