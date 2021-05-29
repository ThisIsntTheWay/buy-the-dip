import requests
import time
import sqlite3
import json
import hmac
import hashlib
import asyncio

import nest_asyncio
nest_asyncio.apply()

import modules.discordBot as dBot
import modules.configuration as modConfig
import modules.database as modDb
import modules.utils as utils
import modules.exchanges.binance as modBinance

# =======================================================
# ===       INIT                                      ===
# =======================================================

intervalStart = int(time.time())

# =======================================================
# ===       FUNC                                      ===
# =======================================================

def newInterval():
    print(utils.getTime() + " [INFO] New interval!")
    intervalStart = int(time.time())

    # Populate modConfig.intervalPrice[] after clearing it
    modConfig.intervalPrice.clear()

    if (modConfig.data["exchanges"]["binance"]["enabled"]):
        for i in range(len(modConfig.tickersBinance)):
            modConfig.intervalPrice.append( modConfig.basePrice( 'Binance', modConfig.tickersBinance[i], int(float(modBinance.binance.getPrice(modConfig.tickersBinance[i]))), False ) )

# ------------------------------
#  Async

async def intervalMonitor():
    # Inform discord of bot going online
    await asyncio.sleep(5)
    
    msg = "Sniper now snipin' for dips...\n"
    if (modConfig.data["exchanges"]["binance"]["enabled"]):
        msg += "Binance: `" + str(modConfig.tickersBinance) + "`, stake: `" + str(modConfig.data["exchanges"]["binance"]["stake"]) + "` \n"
    if (modConfig.data["exchanges"]["kraken"]["enabled"]):
        msg += "Kraken: `" + str(modConfig.tickersKraken) + "`, stake: `" + str(modConfig.data["exchanges"]["binance"]["stake"]) + "` \n"
    msg += "Interval: `" + str(modConfig.interval) + " seconds`, dip threshold: `" + str(modConfig.dipThreshold) + "%`"
    
    await client.send_message(msg)
    
    while True:
        await asyncio.sleep(1)
        # Check if an interval has passed
        if (int(time.time()) - intervalStart) > modConfig.interval:
            newInterval()

# =======================================================
# ===       MAIN                                      ===
# =======================================================

print(utils.getTime() + " [INFO] Interval set at: " + str(modConfig.interval) + " seconds.")
print(utils.getTime() + " [INFO] Percentage threshhold: " + str(modConfig.dipThreshold) + "%")
print(utils.getTime() + " [LOOP] Beginning...")
newInterval()

# Create tasks within discord.py asyncio loop
dBot.client.loop.create_task(intervalMonitor())
dBot.client.loop.create_task(modBinance.binanceMonitor())
dBot.client.run(modConfig.data["discord"]["token"])

print("END OF SCRIPT")

#dBot.client.loop.create_task(dBot.taskDiscord(str(modConfig.data["discord"]["channel"])))
#dBot.client.run(str(modConfig.data["discord"]["token"]))
