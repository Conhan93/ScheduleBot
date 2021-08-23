import asyncio
from discord.ext import tasks
from schedulebot import ScheduleBot
import datetime
import os



scheduleclient = ScheduleBot()

@tasks.loop(hours=1)
async def update_schedule_monday():
    if not scheduleclient.is_ready():
        return

    print("looping")
    if datetime.datetime.now().hour == 7 and datetime.datetime.today().weekday() == 0:

        channel = scheduleclient.get_channel(os.getenv('CHANNEL_IOT20'))
        msg = scheduleclient.get_schedule_current("iot20")

        if len(msg) == 0:
            msg = "kunde inte hitta ett schema för den här veckan"

        print("message is : " + msg)
        await channel.send(msg)
    
    print("loop done")
            
update_schedule_monday.start()

scheduleclient.run(os.getenv('DISCORD_TOKEN'))

