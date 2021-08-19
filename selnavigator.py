# navigation selenium
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class SelNavigator:
    """ Navigates the TimeEdit page """

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
        """ Gets the schedule page for the current week """
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
        """ Gets the schedule page for the given week """
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