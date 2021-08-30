import os

import discord
from discord.ext import tasks

from .selnavigator import SelNavigator
from .pageparser import PageParser
from .settings import Settings


from datetime import datetime as time
import pytz

import asyncio


class ScheduleBot(discord.Client):
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings = Settings()

        self.classname = None
        self.week = None
         

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))

        self.loop.create_task(self.post_schedule_loop())

    async def on_message(self, message):
        """ triggers on message from discord """

        if message.author == self.user:
            return
        
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


    async def send_message_to_channel(self, channel_id, msg):
        try:
            if len(msg) > 0:
                channel = self.get_channel(channel_id)
                await channel.send(msg)
        except Exception as error:
            print(repr(error))
        
    async def post_schedule_loop(self):
        if not self.is_ready():
            await self.wait_until_ready()

        while True:
            print("looping")
            
            if time.now(pytz.timezone('Europe/Stockholm')).hour == 9 and time.today().weekday() == self.settings.weekday['mon']:
                
                msg_iot20 = self.get_schedule_for_week(str(time.today().isocalendar()[1]), 'iot20')
                msg_iot21 = self.get_schedule_for_week(str(time.today().isocalendar()[1]), 'iot21')

                await self.send_message_to_channel(self.settings.channels['iot20'], msg_iot20)

                await self.send_message_to_channel(self.settings.channels['iot'], msg_iot21)
                await self.send_message_to_channel(self.settings.channels['iot'], msg_iot20)          
            
            print("loop done")
            await asyncio.sleep(self.settings.hour)
    
    def get_schedule_for_week(self, week, classname):
        """" Gets class schedule for given week """
        navigator = SelNavigator()
        parser = PageParser()
        page = navigator.get_page_at(week, classname)

        
        return parser.extract_schedule(page)
    def get_schedule_current(self, classname):
        """" Gets class schedule for current week """
        navigator = SelNavigator()
        parser = PageParser()
        page = navigator.get_page(classname)

        
        return parser.extract_schedule(page)
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