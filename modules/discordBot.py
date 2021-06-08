# Discord bot module

import discord
import asyncio
from discord.ext.commands import Bot

import modules.utils as utils
import modules.configuration as config
    
discordActive = config.data["discord"]["enabled"]

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

@client.command(pass_context = True)
async def clear(ctx, number):
    print("clear called")
    number = int(number) #Converting the amount of messages to delete to an integer
    counter = 0
    async for x in client.logs_from(ctx.message.channel, limit = number):
        if counter < number:
            await client.delete_message(x)
            counter += 1
            await asyncio.sleep(1.2) #1.2 second timer so the deleting process can be even

        
# Function to send a discord bot message from external modules
# Required because a circular import would fuck things up
async def sendMsgByProxy(msg):
    if discordActive:
        channel = client.get_channel(int((config.data["discord"]["channel"])))
        await channel.send(msg)
