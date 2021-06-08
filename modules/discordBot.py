# Discord bot module
from discord.ext.commands import Bot

import modules.utils as utils
import modules.configuration as config
    
discordActive = config.data["discord"]["enabled"]
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

@client.command()
async def percentage(ctx, ticker):
    print("percentage")
    ticker = str(ticker)
    
    await ctx.send('Percentage for this ticker is: ')

        
# Function to send a discord bot message from external modules
# Required because a circular import would fuck things up
async def sendMsgByProxy(msg):
    if discordActive:
        channel = client.get_channel(int((config.data["discord"]["channel"])))
        await channel.send(msg)
