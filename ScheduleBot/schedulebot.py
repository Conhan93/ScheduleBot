import discord

from .selnavigator import SelNavigator
from .pageparser import PageParser
from .settings import Settings
from .util import time
from .Models import Schedule

import asyncio

import argparse
import shlex
import io

class ScheduleBot(discord.Client):
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings = Settings()
        self.navigator = SelNavigator(self.settings)

        self.classname = None
        self.week = None
         

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))

        self.loop.create_task(self.post_schedule_loop())

    async def on_message(self, message):
        """ triggers on message from discord """

        if message.author == self.user:
            return
        
        if message.content.startswith('$schedulebot'):


            try:
                response = self._get_args(message.content)

                # get schedule for current week
                if self.classname and not self.week:
                    response = self.get_schedule_for_week(str(time.get_cur_week()), self.classname)
                # get schedule for given week
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
            # wait for an hour
            await asyncio.sleep(self.settings.hour)

            if time.get_cur_week() not in self.settings.schoolweeks: 
                continue

            if time.get_cur_hour() == 6 and time.get_cur_weekday() == self.settings.weekday['mon']:
                    
                week = str(time.get_cur_week())

                # get schedules
                msg_iot20 = self.get_schedule_for_week(week, 'iot20')
                msg_iot21 = self.get_schedule_for_week(week, 'iot21')

                # post schedules to schedule channels
                await self.send_message_to_channel(self.settings.channels['iot20'], msg_iot20)

                await self.send_message_to_channel(self.settings.channels['iot'], msg_iot21)
                await self.send_message_to_channel(self.settings.channels['iot'], msg_iot20)          
    
    def get_schedule_for_week(self, week, classname):
        """" Gets class schedule for given week """
        parser = PageParser()
        page = self.navigator.get_page_at(week, classname)
        entries = parser.extract_schedule(page)
        _schedule = Schedule(entries)

        return _schedule.__repr__()
        
    def get_schedule_current(self, classname):
        """" Gets class schedule for current week """
        parser = PageParser()
        page = self.navigator.get_page(classname)

        
        return parser.extract_schedule(page)
    def _get_args(self, _input):
        split_input = shlex.split(_input)

        # remove $schema
        split_input.pop(0)

        # add help arg to display help message if no args provided
        if len(split_input) == 0:
            split_input.append('-h')

        argparser = argparse.ArgumentParser(prog='$schedulebot')
        argparser.add_argument('-w','--week', help='week number')
        argparser.add_argument('-c', '--classname',required=True,help='required! name of the class or group, ex. "iot20')
        
        try:
            args = argparser.parse_args(split_input)

            self.classname = args.classname
            self.week = args.week
        except:
            help_io = io.StringIO()

            # save help message in help_io
            argparser.print_help(help_io)

            help_message = help_io.getvalue()
            help_io.close()
            return help_message

    def _reset_variables(self):
        self.classname = None
        self.week = None