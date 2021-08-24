import asyncio
import threading
from extractor import Extractor
import discord
import datetime
import threading
from time import sleep

from selnavigator import SelNavigator
from discord.ext import tasks
from datetime import datetime as time
import pytz
import os

class ScheduleBot(discord.Client):
   
    def __init__(self, *args, **kwargs):
         self.classname = None
         self.week = None
         super().__init__(*args, **kwargs)

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))

        self.loop.create_task(self.update_schedule_monday())
        #self.update_schedule_monday().start()

    async def on_message(self, message):
        """ triggers on message from discord """

        if message.author == self.user:
            return

        await self.HandleMessage(message)
        
    @tasks.loop(hours=1)
    async def update_schedule_monday(self):
        if not self.is_ready():
            await self.wait_until_ready()

        print("looping")
        
        if time.now(pytz.timezone('Europe/Stockholm')).hour == 20 and time.today().weekday() == 1:

            channel = self.get_channel(os.getenv(int('CHANNEL_IOT20')))
            msg_iot20 = self.get_schedule_for_week(str(time.today().isocalendar()[1]), 'iot20')

            if len(msg_iot20) == 0:
                msg_iot20 = "kunde inte hitta ett schema för den här veckan"
            else:
                await channel.send(msg_iot20)

            channel = self.get_channel(os.getenv(int('CHANNEL_IOT')))
            msg_iot = self.get_schedule_for_week(str(time.today().isocalendar()[1]), 'iot20')

            if len(msg_iot) == 0:
                msg_iot = "kunde inte hitta ett schema för den här veckan"
            else:
                await channel.send(msg_iot)
                await channel.send(msg_iot20)

            print("message is : " + msg_iot)
            
        
        print("loop done")
    
    def get_schedule_for_week(self, week, classname):
        """" Gets class schedule for given week """
        navigator = SelNavigator()
        extractor = Extractor()
        page = navigator.get_page_at(week, classname)

        
        return extractor.extract_schedule(page)
    def get_schedule_current(self, classname):
        """" Gets class schedule for current week """
        navigator = SelNavigator()
        extractor = Extractor()
        page = navigator.get_page(classname)

        
        return extractor.extract_schedule(page)
    def _get_args(self, args):
        argsl = args.split()

        
        if len(argsl) < 2 and len(argsl) > 3:
            raise ValueError('invalid amount of arguments')
        
        if len(argsl) == 2:
            self.classname = argsl[1]
        else:
            self.classname = argsl[1]
            self.week = argsl[2]

    def _reset_variables(self):
        self.classname = None
        self.week = None

    async def HandleMessage(self, message):
        if message.content.startswith('$schema'):

            if 'help' in message.content.lower():
                await message.channel.send('skriv "$schema klassnamn(ex iot20) vecka(34)" för schema')
                return

            try:
                self._get_args(message.content)
                
                if self.classname and not self.week:
                    response = self.get_schedule_current(self.classname)
                elif self.classname and self.week:
                    response = self.get_schedule_for_week(self.week, self.classname)
        
                if len(response) == 0:
                    await message.channel.send('kunde inte hitta ett schema för den veckan')
                    
                else:
                    await message.channel.send(response)
                
            # print exception to log
            except Exception as error:
                print(f'wooops : {repr(error)}')
            
            self._reset_variables()