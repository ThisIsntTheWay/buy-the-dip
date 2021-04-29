# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
with open('.\tokens\discord.txt') as f:
    TOKEN = f.readlines()

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)