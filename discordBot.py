# bot.py
import discord
import asyncio
import json

with open('configuration.json') as config:
    data = json.load(config)
    

class SniperGuy(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.bgTask())

    async def on_ready(self):
        print('DISCORD: Logon was successful: ' + self.user.name + ' / ' + str(self.user.id))

    async def bgTask(self):
        #await self.wait_until_ready()
        counter = 0
        channel = self.get_channel(data["discord"]["channel"]) # channel ID goes here
        while not self.is_closed():
            counter += 1
            await channel.send(counter)
            await asyncio.sleep(3) # task runs every 60 seconds