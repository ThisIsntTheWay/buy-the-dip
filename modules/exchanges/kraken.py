# Kraken module

import asyncio
import hmac
import hashlib
import requests
import time
import base64
import urllib.parse

import modules.utils as utils
import modules.configuration as modConfig
import modules.discordBot as dBot

krakenAPI = "https://api.kraken.com/0/"

async def krakenMonitor():
    await asyncio.sleep(8)
    
    while True:
        await asyncio.sleep(3)
        print(utils.getTime() + " [PRIC] Querying kraken...")
        
        for i in range(len(modConfig.tickersKraken)):
            priceNow = int(float(kraken.getPrice(modConfig.tickersKraken[i])))

            # Check if the price is below the dip threshold            
            for base in modConfig.intervalPrice:
                if base.exchange == "Kraken" and base.ticker == modConfig.tickersKraken[i]:
                    percentage = 100 * (priceNow - base.price) / base.price
                    print(utils.getTime() + "   > " + modConfig.tickersKraken[i] + ": " + str(priceNow) + " - change: " + str(round(percentage, 2)) + "%")
                    
                    # Buy if the price has dipped below threshold and nothing has been bought before
                    if percentage < modConfig.dipThreshold and not base.bought:
                        print(utils.getTime() + "       > Percentage below threshold, buying!")
                        
                        # Notify discord
                        msg = "Attempting to buy **" + base.ticker + "** at a price of **" + str(priceNow) + "** *(" + str(int(percentage))+ "%)* on **" + base.exchange + "**..."
                        await dBot.sendMsgByProx(msg)
                        
                        # Attempt to buy and otify discord and console about result
                        msg, status = kraken.buy(base.ticker, priceNow)
                        await dBot.sendMsgByProx("@here " + msg)
                        print(utils.getTime() + " " + msg)
                            
                        base.bought = True

def getSignature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()
# ------------------------------
#  Classes

class Kraken:    
    # Acquire price
    def getPrice(self, ticker):
        response = requests.get(krakenAPI + str("public/Ticker?pair=") + str(ticker))
        
        # Handle response
        if response.status_code == 200:
            # Kraken is hipster and doesn't necessarily return a ticker we except (Eg: I want BTCUSDT, I get *XXBT*USD)
            # As such, we need to save all keys on the second level (after 'result') into a list and access the first index, which is the ticker we want.
            # It's stupid >:(
        
            rTicker = list(response.json()["result"].keys())[0]
            return response.json()['result'][rTicker]['o']
        else:
            return "HTTP/" + str(response.status_code) + " - " + str(response.json()), False
    
    def buy(self, ticker, priceNow):
        stake = modConfig.data["exchanges"]["kraken"]["stake"]
        URI = krakenAPI + "private/AddOrder"
        
        # Assemble request body
        requestBody = {
            "nonce": str(int(1000*time.time())),
            "ordertype": "market",
            "type": "buy",
            "volume": stake / priceNow,
            "pair": ticker,
            "validate": True
        }
                #print(utils.getTime() + " [INFO] " + fullRequest)
        
        # Construct API signature
        signature = getSignature(URI, requestBody, modConfig.data["exchanges"]["kraken"]["api_secret"])
        
        # Send POST
        headers = {
            'API-Key': modConfig.data["exchanges"]["kraken"]["api_key"],
            'API-Sign': signature
        }
        response = requests.post(URI, headers=headers, data=requestBody)
        
        # Handle response
        if response.status_code == 200:
            return "\u2705 " + str(response.json()), True
        else:
            return "\u274C " + str(response.json()['result']), False        

# Create instances
kraken = Kraken()