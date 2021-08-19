from schedulebot import ScheduleBot
import os


scheduleclient = ScheduleBot()
scheduleclient.run(os.getenv('DISCORD_TOKEN'))
