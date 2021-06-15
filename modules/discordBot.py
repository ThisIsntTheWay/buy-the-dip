# Discord bot module
import time
import os
import sys

from discord.ext.commands import Bot
from discord.ext.commands import MissingPermissions
from discord.ext.commands import has_permissions

import modules.utils as utils
import modules.configuration as modConfig
    
discordActive = modConfig.data["discord"]["enabled"]
percentageBuffer = []

client = Bot('!')

# Events
@client.event
async def on_ready():
    print(utils.getTime() + ' [BOT] Successful login as {0.user}'.format(client))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Permit processing of @client.command() stuff
    await client.process_commands(message)
    
# Commands
@client.command(name='ping', help='Have the bot confirm it\'s still alive.', pass_context=True)
async def ping(ctx):
    utils.log("[BOT] Heartbeat requested.")
    await ctx.reply("Pong!", mention_author=True)
    

@client.command(name='show_config', help='Show the running configuration.')
async def show_config(ctx):
    utils.log("[BOT] Display running config.")
    msg = ""
    if (modConfig.data["exchanges"]["binance"]["enabled"]):
        msg += "> Binance: `" + str(modConfig.tickersBinance) + "`, stake: `" + str(modConfig.data["exchanges"]["binance"]["stake"]) + "` \n"
    if (modConfig.data["exchanges"]["kraken"]["enabled"]):
        msg += "> Kraken: `" + str(modConfig.tickersKraken) + "`, stake: `" + str(modConfig.data["exchanges"]["kraken"]["stake"]) + "` \n"
    msg += "> Timeframe: `" + str(modConfig.timeframe / 3600) + "h`, dip threshold: `" + str(modConfig.dipThreshold) + "%`"
    
    await ctx.reply(msg, mention_author=False)

@client.command(name='percentage', help='Get price change as percentage of specified ticker.')
async def percentage(ctx, ticker=None):
    utils.log("[BOT] Query percentage changes.")
    if ticker is None:
        return await ctx.send('Missing argument: `ticker`')
    
    print("percentage")
    ticker = str(ticker)
    
    await ctx.send('Percentage for this ticker is: ')
    
@client.command(name='timeframe', help='Get time left in the current timeframe.')
async def timeframe(ctx):
    utils.log("[BOT] Display timeframe.")
    
    timeDiff = modConfig.timeframe - (int(time.time()) - modConfig.timeframeStart) 
    msg = "Timeframe (`"+ str(modConfig.timeframe / 3600) +"h`) will expire in: `" + str(round(timeDiff / 3600, 2)) + "h` / `" + str(timeDiff) + "s`."
    
    await ctx.send(msg)
    
@client.command(name="status", help="Get status of bot.")
async def status(ctx):
    utils.log("[BOT] Query status.")
    if modConfig.canRun:
        lastUpdate = int(time.time()) - modConfig.lastUpdate
        
        msg = "The bot is running.\nLast update: `" + str(lastUpdate) + "s` ago."
        await ctx.send(msg)        
    else:
        await ctx.send("The bot is halted.")
    
@client.command(name='stop', help='Halt the bot.')
@has_permissions(manage_messages=True)  
async def timeframe(ctx):
    utils.log("[BOT] Pausing the bot.")
    
    if modConfig.canRun:
        await ctx.send("Bot has been halted!")
        modConfig.canRun = False
    else:
        await ctx.send("The bot is already halted.")
        
@client.command(name='reset', help='Restart the bot.')
@has_permissions(manage_messages=True)
async def reset(ctx):
    utils.log("[BOT] Restarting the bot.")
    await ctx.send("Restarting bot...")
    try:
        os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        await ctx.send("Could not restart the bot: " + str(e) + "\nThe current session will continue.")
        
@client.command(name='start', help='Start/Resume the bot.')
@has_permissions(manage_messages=True)  
async def timeframe(ctx):
    utils.log("[BOT] Resuming the bot.")
    
    if not modConfig.canRun:
        await ctx.send("Resuming the bot!")
        modConfig.canRun = True
    else:
        await ctx.send("The bot is already running.")

@client.command(name='nuke', help='Completely nuke text channel.')
@has_permissions(manage_messages=True)  
async def nuke(ctx):
    utils.log("[BOT] Nuking current channel.")
    
    await ctx.channel.purge(limit=600)
    await ctx.send('Done purging this channel.')        
    
@nuke.error
async def nuke_error(error, ctx):
   if isinstance(error, MissingPermissions):
       await ctx.send("You are not authorized to use this command.")

# Function to send a message using the discord bot from external modules
# Required because a circular import would fuck things up otherwise
async def sendMsgByProxy(msg):
    if discordActive:
        channel = client.get_channel(int((modConfig.data["discord"]["channel"])))
        await channel.send(msg)
