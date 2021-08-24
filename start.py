from discord.ext import tasks
from schedulebot import ScheduleBot
import os

from datetime import datetime as time
import pytz



scheduleclient = ScheduleBot()

scheduleclient.run(os.getenv('DISCORD_TOKEN'))


