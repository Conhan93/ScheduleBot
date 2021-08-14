from bs4 import BeautifulSoup
from urllib.request import urlopen




# navigation selenium
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class SelNavigator:
    def __init__(self):
        self.url = os.getenv('TIMEEDIT_URL')
    
    def _enter_classname(self, classname):
         #find search box
        search_field = self.driver.find_element_by_id('ffsearchname')

        # enter search text and click on search button
        search_field.send_keys(classname)
        self.driver.find_element_by_class_name('ffsearchbutton').click()
        #WebDriverWait(self.driver, 2) # wait 2 sec
        search_field.send_keys(Keys.ENTER) # hit enter - needed for some reason

    def _select_search_result(self):
        # wait 2 sec and click on first search result

        try:
            element = WebDriverWait(self.driver, 5).until(
        EC.presence_of_element_located((By.ID, "objectbasketitemX0"))
        )
        finally:
            try:
                self.driver.find_element_by_id('objectbasketitemX0').click()
            except:
                
                return 0
        
        # click on "visa schema"
        #WebDriverWait(self.driver, 2)
        self.driver.find_element_by_id('objectbasketgo').click()

        return 1
    def _load_driver(self):
        options = webdriver.FirefoxOptions()
	
        # enable trace level for debugging 
        options.log.level = "trace"

        options.add_argument("-remote-debugging-port=9224")
        options.add_argument("-headless")
        options.add_argument("-disable-gpu")
        options.add_argument("-no-sandbox")

        binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))

        firefox_driver = webdriver.Firefox(
            firefox_binary=binary,
            executable_path=os.environ.get('GECKODRIVER_PATH'),
            options=options)

        return firefox_driver

    def get_page(self, classname):
        # setup browser
        self.driver = self._load_driver()
        #load page
        self.driver.get(self.url)

        self._enter_classname(classname)
        if self._select_search_result() == 0:
            return ''

        #WebDriverWait(self.driver, 2)
        week = self.driver.find_element_by_class_name('flexFixed')
        html = week.get_attribute('innerHTML')

        page = self.driver.page_source
        self.driver.close()
        return page

    def get_page_at(self, week_sel, classname):
        # setup browser
        self.driver = self._load_driver()

        #load page
        self.driver.get(self.url)

        
        self._enter_classname(classname)
        if self._select_search_result() == None:
            return ''
        
        #WebDriverWait(self.driver, 2)
        week = self.driver.find_element_by_class_name('flexFixed')
        html = week.get_attribute('innerHTML')

        #WebDriverWait(self.driver, 2)
        count = 0
        while 'v '+ week_sel not in html and count < 30:
            self.driver.find_element_by_class_name('btrRight').click()
            week = self.driver.find_element_by_class_name('flexFixed')
            html = week.get_attribute('innerHTML')
            count += 1

        page = self.driver.page_source
        self.driver.close()
        return page

class ScheduleBot:
   
    def __init__(self):
         self.url = 'https://cloud.timeedit.net/nackademin/web/1/ri13566y6Z6830Q067QQY505Z467078Q961W25.html'

         self.classname = None
         self.week = None

    def relevant_rows(self,tag):
        return tag.has_attr('class') and tag.has_attr('data-id') and tag.has_attr('tabindex') and tag.has_attr('onclick')
    
    def _format_output(self, textlines):
        results = []
        index = 0
        while index + 1 < len(textlines):
            results.append(textlines[index].replace('\n',' ') + '\n\t' + textlines[index+1].replace('\n', ' '))
            index += 2

        return str.join('\n\n', results)

    def _get_soup(self):
        page = urlopen(self.url)
        html = page.read().decode("utf-8")
        return BeautifulSoup(html, "html.parser")

    def _get_text_lines(self, soup):
        textlines = []
        lines = soup.find_all(self.relevant_rows)
        textlines = [line.get_text() for line in lines]
        return [str(line).strip() for line in textlines]

    def getSchedule(self):
        
        soup = self._get_soup()

        
        textlines = self._get_text_lines(soup)

        output = self._format_output(textlines)
        
        return output
    
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