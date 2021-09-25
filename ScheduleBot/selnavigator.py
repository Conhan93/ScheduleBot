# navigation selenium
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.firefox.webelement import FirefoxWebElement

class SelNavigator:
    """ Navigates the TimeEdit page """

    def __init__(self, settings):

        self.settings = settings
        self.url = self.settings.url 
    
    def _enter_classname(self, classname):
         #find search box
        search_field = self.driver.find_element_by_id('ffsearchname')

        # enter search text and click on search button
        search_field.send_keys(classname)
        self.driver.find_element_by_class_name('ffsearchbutton').click()

        search_field.send_keys(Keys.ENTER) # hit enter - needed for some reason

    def _select_search_result(self):
        """ Selects the first search result on the page """

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

        binary = FirefoxBinary(self.settings.firefox_binary)

        firefox_driver = webdriver.Firefox(
            firefox_binary=binary,
            executable_path=self.settings.driver_path,
            options=options)

        return firefox_driver

    def get_page(self, classname):
        """ Gets the schedule page for the current week """
        # setup browser
        self.driver = self._load_driver()
        #load page
        self.driver.get(self.url)

        self._enter_classname(classname)
        if self._select_search_result() == 0:
            return ''

        week = self.driver.find_element_by_class_name('flexFixed')
        html = week.get_attribute('innerHTML')

        data = self._get_table_data()
        self.driver.quit()
        
        return data

    def get_page_at(self, week_sel, classname):
        """ Gets the schedule page for the given week """
        # setup browser
        self.driver = self._load_driver()

        #load page
        self.driver.get(self.url)

        
        self._enter_classname(classname)
        if self._select_search_result() == None:
            return ''
        
        week = self.driver.find_element_by_class_name('flexFixed')
        html = week.get_attribute('innerHTML')

        count = 0
        while 'v '+ week_sel not in html and count < 30:
            self.driver.find_element_by_class_name('btrRight').click()
            week = self.driver.find_element_by_class_name('flexFixed')
            html = week.get_attribute('innerHTML')
            count += 1

        data = self._get_table_data()
        self.driver.quit()
        
        return data
    
    def get_page_at_date(self, search_date, classname):
        #setup browser
        self.driver = self._load_driver()

        #load page
        self.driver.get(self.url)

        self._enter_classname(classname)
        if self._select_search_result() == None:
            return ''

       
        count = 0
        while count < 30:
            
            dates = [tag.text for tag in self.driver.find_elements(By.XPATH, '//table[@class="restable"]/tbody/tr[@class="rr clickable2"]/td[3]')]
            
            if search_date in dates:
                break
            
            self.driver.find_element_by_class_name('btrRight').click()
            count += 1

        data = self._get_entries_by_date(search_date)
        self.driver.quit()
        
        return data
    

    def _get_table_data(self):

        data = []

        table = self.driver.find_element(By.XPATH, '//table[@class="restable"]/tbody')

        for row in table.find_elements(By.XPATH, './/tr[@class="rr clickable2"]'):
            event = []
            for col in row.find_elements(By.XPATH, './/td'):
                event.append(col.text)
            data.append(event)
 
        return data
    
    def _get_entries_by_date(self, date):

        data = []

        read = False

        table = self.driver.find_element(By.XPATH, '//table[@class="restable"]/tbody')

        for row in table.find_elements(By.XPATH, './/tr[@class="rr clickable2"]'):
            
            columns = row.find_elements(By.XPATH, './/td')

            if len(columns[2].text) > 0:
                read = True if columns[2].text == date else False

            if not read:
                continue
            
            # add row to list
            data.append([col.text for col in columns])
 
        return data
            