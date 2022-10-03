import discord

from ScheduleBot.schedulebot import ScheduleBot
from ScheduleBot.config import config




intents = discord.Intents.default()
intents.members = True
intents.message_content = True

scheduleclient = ScheduleBot(intents=intents)

scheduleclient.run(config.discordToken)


