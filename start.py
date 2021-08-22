import asyncio
from schedulebot import ScheduleBot
import os



scheduleclient = ScheduleBot()

asyncio.get_event_loop().create_task(scheduleclient.update_schedule_monday)

scheduleclient.run(os.getenv('DISCORD_TOKEN'))
