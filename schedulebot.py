import threading
from extractor import Extractor
import discord
import datetime
import threading
from time import sleep

from selnavigator import SelNavigator

class ScheduleBot(discord.Client):
   
    def __init__(self, *args, **kwargs):
         self.classname = None
         self.week = None
         super().__init__(*args, **kwargs)

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))

        self.timer = threading.Thread(None, self.update_schedule_monday) 
        self.timer.start()
       
    
    def update_schedule_monday(self):
        while True:
            if datetime.datetime.now().hour == 17:
                print("clk is")
                if datetime.datetime.today().weekday() == 6:
                    print("it's sunday")
            sleep(5)
                

    async def on_message(self, message):
        """ triggers on message from discord """

        if message.author == self.user:
            return

        await self.HandleMessage(message)
    
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