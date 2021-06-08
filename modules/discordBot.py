# Discord bot module

import discord
import time
import json

import modules.utils as utils
import modules.configuration as config
    
discordActive = config.data["discord"]["enabled"]

# Bot class
class SniperGuy(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    async def on_ready(self):
        print(utils.getTime() + ' [BOT ] Login was successful: ' + self.user.name + ' / ' + str(self.user.id))
        
    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!ping'):
            await message.reply('Pong', mention_author=True)
            
    async def send_message(self, message):
        channel = self.get_channel(int((config.data["discord"]["channel"])))
        await channel.send(message)

client = SniperGuy()
        
# Function to send a discord bot message from external modules
# Required because a circular import would fuck things up
async def sendMsgByProx(msg):
    if discordActive:
        await client.send_message(msg)
