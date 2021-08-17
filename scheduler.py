import discord
from discord.ext import commands

from selnavigator import SelNavigator
from bs4 import BeautifulSoup

class ScheduleBot(discord.Client):
   
    def __init__(self, *args, **kwargs):
         self.classname = None
         self.week = None
         super().__init__(*args, **kwargs)

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))

    async def on_message(self, message):
        if message.author == self.user:
            return

        await self.HandleMessage(message) # go to schedule

    def relevant_rows(self,tag):
        return tag.has_attr('class') and tag.has_attr('data-id') and tag.has_attr('tabindex') and tag.has_attr('onclick')
    
    def _format_output(self, textlines):
        results = []
        index = 0
        while index + 1 < len(textlines):
            results.append(textlines[index].replace('\n',' ') + '\n\t' + textlines[index+1].replace('\n', ' '))
            index += 2

        return str.join('\n\n', results)

    def _get_text_lines(self, soup):
        textlines = []
        lines = soup.find_all(self.relevant_rows)
        textlines = [line.get_text() for line in lines]
        return [str(line).strip() for line in textlines]
    
    def get_schedule_for_week(self, week, classname):
        navigator = SelNavigator()
        page = navigator.get_page_at(week, classname)

        soup = BeautifulSoup(page, "html.parser")

        textlines = self._get_text_lines(soup)

        output = self._format_output(textlines)
        
        return output
    def get_schedule_current(self, classname):
        navigator = SelNavigator()
        page = navigator.get_page(classname)

        soup = BeautifulSoup(page, "html.parser")

        textlines = self._get_text_lines(soup)

        output = self._format_output(textlines)
        
        return output
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
                    await message.channel.send('kunde inte hitta ett schema')
                    
                else:
                    await message.channel.send(response)
                    print(response)
                

            except Exception as error:
                print(f'wooops : {repr(error)}')
            
            self._reset_variables()