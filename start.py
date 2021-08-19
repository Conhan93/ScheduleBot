from schedulebot import ScheduleBot
import discord
from discord.ext import commands
import os


#client = discord.Client()

scheduleclient = ScheduleBot()
scheduleclient.run(os.getenv('DISCORD_TOKEN'))

"""
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await scheduleclient.HandleMessage(message) # go to schedule

client.run(os.getenv('DISCORD_TOKEN'))
"""
