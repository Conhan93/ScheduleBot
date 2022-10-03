import os
from .config import config


class Settings:
    """Holds settings, config and constant values"""

    def __init__(self):

        self.init_time_settings()
        self.init_channels_settings()
        self.init_navigator_settings()

    def init_time_settings(self):

        self.hour = 60*60

        self.weekday = {'mon' : 0, 'tue' : 1 , 'wed' : 2,
                        'thu' : 3, 'fri' : 4, 'sat' : 5, 'sun' : 6}

        self.schoolweeks = [i for i in range(34, 53)]
        self.schoolweeks.extend([i for i in range(0,25)])

    def init_channels_settings(self):

        self.channels = {}
        
        self.channels['iot20'] = config.iot20Id
        self.channels['iot'] = config.iotId

    def init_navigator_settings(self):

        self.url = config.url

        # navigator firefox webdrive settings
        self.firefox_binary = os.environ.get('FIREFOX_BIN')
        self.driver_path = os.environ.get('GECKODRIVER_PATH')