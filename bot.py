# Main thing

import time
import asyncio

import nest_asyncio
nest_asyncio.apply()

import modules.discordBot as dBot
import modules.configuration as modConfig
import modules.database as modDb
import modules.utils as utils
import modules.exchanges.binance as modBinance
import modules.exchanges.kraken as modKraken

# =======================================================
# ===       INIT                                      ===
# =======================================================

timeframeStart = int(time.time())

# =======================================================
# ===       FUNC                                      ===
# =======================================================

def newInterval():
    utils.log("[INFO] New timeframe!")
    timeframeStart = int(time.time())

    # Populate modConfig.timeframePrice[] after clearing it
    modConfig.timeframePrice.clear()
    if (modConfig.data["exchanges"]["binance"]["enabled"]):
        for i in range(len(modConfig.tickersBinance)):
            modConfig.timeframePrice.append(
                modConfig.basePrice(
                    'Binance', 
                    modConfig.tickersBinance[i],
                    int(float(modBinance.binance.getPrice(modConfig.tickersBinance[i]))),
                    False,
                    0
                )
            )
            
    if (modConfig.data["exchanges"]["kraken"]["enabled"]):
        for i in range(len(modConfig.tickersKraken)):
            modConfig.timeframePrice.append(
                modConfig.basePrice(
                    'Kraken', 
                    modConfig.tickersKraken[i],
                    int(float(modKraken.kraken.getPrice(modConfig.tickersKraken[i]))),
                    False,
                    0
                )
            )

# ------------------------------
#  Async

async def intervalMonitor():
    # Inform discord of bot going online
    await asyncio.sleep(5)
    
    msg = "**Sniper now snipin' for dips...**\n"
    if (modConfig.data["exchanges"]["binance"]["enabled"]):
        msg += "> Binance: `" + str(modConfig.tickersBinance) + "`, stake: `" + str(modConfig.data["exchanges"]["binance"]["stake"]) + "` \n"
    if (modConfig.data["exchanges"]["kraken"]["enabled"]):
        msg += "> Kraken: `" + str(modConfig.tickersKraken) + "`, stake: `" + str(modConfig.data["exchanges"]["kraken"]["stake"]) + "` \n"
    msg += "> Timeframe: `" + str(modConfig.timeframe / 3600) + "h`, dip threshold: `" + str(modConfig.dipThreshold) + "%`"
    
    await dBot.sendMsgByProxy(msg)
    
    while True:
        await asyncio.sleep(1)
        # Check if an interval has passed
        if (int(time.time()) - timeframeStart) > modConfig.timeframe:
            await dBot.sendMsgByProxy("Starting a new timeframe.")
            newInterval()

# =======================================================
# ===       MAIN                                      ===
# =======================================================

utils.log("[INFO] Timeframe set at: " + str(modConfig.timeframe / 3600) + "h.")
utils.log("[INFO] Percentage threshold: " + str(modConfig.dipThreshold) + "%")
utils.log("[NOTE] The first loop is always slower to start!")
utils.log("[LOOP] Beginning...")
newInterval()

# Create tasks within discord.py asyncio loop
dBot.client.loop.create_task(intervalMonitor())
if modConfig.data["exchanges"]["binance"]["enabled"]:
    dBot.client.loop.create_task(modBinance.binanceMonitor())
    
if modConfig.data["exchanges"]["kraken"]["enabled"]:
    dBot.client.loop.create_task(modKraken.krakenMonitor())

if dBot.discordActive:
    dBot.client.run(modConfig.data["discord"]["token"])
else:
    utils.log("[INFO] Discord integration is disabled.")
    dBot.client.loop.run_forever()

utils.log("END OF SCRIPT")

#dBot.client.loop.create_task(dBot.taskDiscord(str(modConfig.data["discord"]["channel"])))
#dBot.client.run(str(modConfig.data["discord"]["token"]))
