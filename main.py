# bot.py
import os
import discord

# Acquire token
f = open("tokens\discord.txt","r")
TOKEN = f.read()

import discord

# Discord client class
class SniperGuy(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = SniperGuy()

async def taskMsg():
    await client.wait_until_ready()
    bsc_channel = client.get_channel(837374595505455124)
    await bsc_channel.send("Sniper ready for duty.")

client.loop.create_task(taskMsg())
client.run(TOKEN)