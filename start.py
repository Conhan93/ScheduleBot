import asyncio
from schedulebot import ScheduleBot
import datetime
import os



scheduleclient = ScheduleBot()

async def update_schedule_monday():
        count = 0

        while True:
            if count > 4:
                break
            if datetime.datetime.now().hour == 18:
                print("clk is")
                if datetime.datetime.today().weekday() == 6:
                    print("it's sunday")
                    channel = scheduleclient.get_channel(877212291056169050)
                    await channel.send(scheduleclient.get_schedule_current("iot20"))
            #sleep(60)
            await asyncio.sleep(60)
            count += 1

asyncio.get_event_loop().create_task(scheduleclient.update_schedule_monday)

scheduleclient.run(os.getenv('DISCORD_TOKEN'))
