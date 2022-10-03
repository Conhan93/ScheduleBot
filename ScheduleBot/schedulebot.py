import discord

from .selnavigator import SelNavigator
from .settings import Settings
from .util import time
from .Models import Schedule

import asyncio
import logging

import argparse
import shlex
import io

import re

class ScheduleBot(discord.Client):
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings = Settings()
        self.navigator = SelNavigator(self.settings)

        self.classname = None
        self.week = None
        self.date = None
         

    async def on_ready(self):
        logging.info('Logged in as {0.user}'.format(self))
        

        self.loop.create_task(self.post_schedule_loop())

    async def on_message(self, message):
        """ triggers on message from discord """

        if message.author == self.user:
            return
        
        if message.content.startswith('$schedulebot'):


            try:
                response = self._get_args(message.content)

                if self.classname:
                    # get schedule for current week
                    if not self.week and not self.date:
                        response = self.get_schedule_for_week(str(time.get_cur_week()), self.classname)
                    # get schedule for given week
                    elif self.week and not self.date:
                        response = self.get_schedule_for_week(self.week, self.classname)
                    #get schedule for given date
                    elif self.date and not self.week:
                        response = self.get_schedule_for_date(self.date, self.classname)
                
                if len(response) == 0:
                    await message.channel.send('kunde inte hitta ett schema för den veckan')
                    
                else:
                    await message.channel.send(response)
                
            # print exception to log
            except Exception as error:
                logging.error(f'wooops : {repr(error)}')
            
            self._reset_variables()


    async def send_message_to_channel(self, channel_id, msg):
        try:
            if len(msg) > 0:
                channel = self.get_channel(channel_id)
                await channel.send(msg)
        except Exception as error:
            logging.error(repr(error))
        
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
                msg_iot21 = self.get_schedule_for_week(week, 'iot21')
                msg_iot22 = self.get_schedule_for_week(week, 'iot22')

                # post schedules to schedule channels
                await self.send_message_to_channel(self.settings.channels['iot'], msg_iot22)
                await self.send_message_to_channel(self.settings.channels['iot'], msg_iot21)

                logging.info("Updated weekly schedule")          
    
    def get_schedule_for_week(self, week, classname):
        """" Gets class schedule for given week """
        entries = self.navigator.get_page_at(week, classname)

        try:
            # construct schedule
            _schedule = Schedule(entries)

            return _schedule
        except:
            # no schedule found
            return ''
    
    def get_schedule_for_date(self, date, classname):
        """ Gets class schedule for given date"""
        entries = self.navigator.get_page_at_date(date, classname)

        try:
            # construct schedule
            _schedule = Schedule(entries)

            return _schedule
        except:
            # no schedule found
            return ''

    def _get_args(self, _input):
        split_input = shlex.split(_input)

        # remove $schema
        split_input.pop(0)

        # add help arg to display help message if no args provided
        if len(split_input) == 0:
            split_input.append('-h')

        argparser = argparse.ArgumentParser(prog='$schedulebot')
        argparser.add_argument('-c', '--classname',required=True,help='required! name of the class or group, ex. "iot20')

        search_group = argparser.add_mutually_exclusive_group()
        search_group.add_argument('-w','--week',type=time.week_type, help='week number')
        search_group.add_argument('-d', '--date', type=time.date_type, help="date to search for")

        
        try:
            args = argparser.parse_args(split_input)

            self.classname = args.classname
            self.week = args.week
            self.date = args.date

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
        self.date = None

    