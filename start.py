from discord.ext import tasks
from schedulebot import ScheduleBot
import os

from datetime import datetime as time
import pytz



scheduleclient = ScheduleBot()

@tasks.loop(hours=1)
async def update_schedule_monday():
    if not scheduleclient.is_ready():
        await scheduleclient.wait_until_ready()

    print("looping")
    
    if time.now(pytz.timezone('Europe/Stockholm')).hour == 8 and time.today().weekday() == 0:

        channel = scheduleclient.get_channel(int(os.getenv('CHANNEL_IOT20')))
        msg = scheduleclient.get_schedule_for_week(str(time.today().isocalendar()[1]), 'iot20')

        if len(msg) == 0:
            msg = "kunde inte hitta ett schema för den här veckan"
        else:
            await channel.send(msg)

        print("message is : " + msg)
        
    
    print("loop done")
            
update_schedule_monday.start()

scheduleclient.run(os.getenv('DISCORD_TOKEN'))

