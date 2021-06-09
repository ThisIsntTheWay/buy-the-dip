# Discord bot module
import time
import asyncio

from discord.ext.commands import Bot

import modules.utils as utils
import modules.configuration as modConfig
    
discordActive = modConfig.data["discord"]["enabled"]
percentageBuffer = []

client = Bot('!')

@client.event
async def on_ready():
    print(utils.getTime() + ' [BOT] Successful login as {0.user}'.format(client))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!ping'):
        await message.reply('Pong', mention_author=True)
    
    # Permit processing of @client.command() stuff
    await client.process_commands(message)

@client.command(name='percentage', help='Get price change as percentage of specified ticker.')
async def percentage(ctx, ticker=None):
    if ticker is None:
        return await ctx.send('Missing argument: `ticker`.')
    
    print("percentage")
    ticker = str(ticker)
    
    await ctx.send('Percentage for this ticker is: ')
    
@client.command(name='timeleft', help='Get time left of the current timeframe.')
async def timeleft(ctx):
    print("timeleft")
    
    timeDiff = modConfig.timeframe - (int(time.time()) - modConfig.timeframeStart) 
    msg = "Timeframe will expire in: `" + str(round(timeDiff / 3600, 2)) + "h / " + str(timeDiff) + "s`."
    
    await ctx.send(msg)

@client.command(name='nuke', help='Completely nuke text channel.')
async def nuke(ctx):
    await ctx.channel.purge(limit=600)
    await ctx.send('Done purging this channel.')

        
# Function to send a discord bot message from external modules
# Required because a circular import would fuck things up
async def sendMsgByProxy(msg):
    if discordActive:
        channel = client.get_channel(int((modConfig.data["discord"]["channel"])))
        await channel.send(msg)
