import asyncio
from discord.ext import tasks
from schedulebot import ScheduleBot
import datetime
import os



scheduleclient = ScheduleBot()

@tasks.loop(minutes=2)
async def update_schedule_monday():
        if datetime.datetime.now().hour == 19:
            print("clk is")
            if datetime.datetime.today().weekday() == 6:
                print("it's sunday")
                channel = scheduleclient.get_channel(877212291056169050)
                await channel.send(scheduleclient.get_schedule_current("iot20"))
        #sleep(60)
        #await asyncio.sleep(60)
            
update_schedule_monday.start()
#timer = asyncio.get_event_loop().create_task(update_schedule_monday())
#asyncio.get_event_loop().run_until_complete(timer)

scheduleclient.run(os.getenv('DISCORD_TOKEN'))
