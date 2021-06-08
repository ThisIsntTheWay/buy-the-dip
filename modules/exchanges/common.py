# Common exchange module

import time
import requests
import asyncio

import modules.utils as utils
import modules.configuration as config
import modules.discordBot as bot
import modules.exchanges.kraken as modKraken
import modules.exchanges.binance as modBinance

async def exchangeMonitor():
    await asyncio.sleep(8)
    
    while True:
        await asyncio.sleep(3)        
        utils.log("[PRIC] Querying prices...")
        
        # Query prices:
        for base in config.timeframePrice:
            if base.exchange == "Binance":
                if base.ticker == config.al
            elif (base.exchange == "Kraken"):
                
            
        try:
            for i in range(len(config.tickersKraken)):
                priceNow = int(float(modKraken.kraken.getPrice(config.tickersKraken[i])))

                # Check if the price is below the dip threshold            
                for base in config.timeframePrice:
                    if base.exchange == "Kraken" and base.ticker == config.tickersKraken[i]:
                        percentage = 100 * (priceNow - base.price) / base.price
                        utils.log("   > " + config.tickersKraken[i] + ": " + str(priceNow) + " - change: " + str(round(percentage, 2)) + "%")
                        
                        # Buy if the price has dipped below threshold and nothing has been bought before
                        if percentage < config.dipThreshold and not base.bought:
                            utils.log("       > Percentage below threshold, buying!")
                            
                            # Notify discord
                            msg = "Attempting to buy **" + base.ticker + "** at a price of **" + str(priceNow) + "** *(" + str(int(percentage))+ "%)* on **" + base.exchange + "**..."
                            await bot.sendMsgByProx(msg)
                            
                            # Attempt to buy and otify discord and console about result
                            msg, status = modKraken.kraken.buy(base.ticker, priceNow)
                            utils.log(msg)
                            await bot.sendMsgByProx("> `" + msg + "` @here")
                                
                            base.bought = True
        except:
            utils.log("Error during exchangeMonitor()")