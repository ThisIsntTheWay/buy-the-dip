# bot.py
import os
import discord

# Acquire token
f = open("tokens\discord.txt","r")
TOKEN = f.read()

# Discord client class
class SniperGuy(discord.Client):
    async def on_ready(self):
        print('DISCORD BOT: Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('DISCORD BOT: Message from {0.author}: {0.content}'.format(message))

# Create discord client
client = SniperGuy()

# Background task
async def taskMsg():
    await client.wait_until_ready()
    bsc_channel = client.get_channel(837374595505455124)
    await bsc_channel.send("Sniping for dips...")

# Because client.run essentially locks up, everything must be done using background tasks.
client.loop.create_task(taskMsg())

client.run(TOKEN)