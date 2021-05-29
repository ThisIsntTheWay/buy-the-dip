# Discord bot module

import discord
import time
import json

with open('configuration.json') as config:
    data = json.load(config)
    
discordActive = data["discord"]["enabled"]
    
def getTime():
    return time.strftime("%H:%M:%S", time.localtime())

class SniperGuy(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    async def on_ready(self):
        print(getTime() + ' [BOT ] Login was successful: ' + self.user.name + ' / ' + str(self.user.id))
        
    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!ping'):
            await message.reply('Pong', mention_author=True)
            
    async def send_message(self, message):
        channel = self.get_channel(int((data["discord"]["channel"])))
        await channel.send(message)

client = SniperGuy()
        
# Function to send a discord bot message from external modules
async def sendMsgByProx(msg):
    if discordActive:
        await client.send_message(msg)