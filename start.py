import os

from ScheduleBot.schedulebot import ScheduleBot


scheduleclient = ScheduleBot()

scheduleclient.run(os.getenv('DISCORD_TOKEN'))


