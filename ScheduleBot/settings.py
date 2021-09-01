import os


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

        self.schoolweeks = list(range(34, 53)).extend(list(range(0, 25)))

    def init_channels_settings(self):

        self.channels = {}
        
        self.channels['iot20'] = int(os.getenv('CHANNEL_IOT20'))
        self.channels['iot'] = int(os.getenv('CHANNEL_IOT'))

    def init_navigator_settings(self):

        self.url = os.getenv('TIMEEDIT_URL')

        # navigator firefox webdrive settings
        self.firefox_binary = os.environ.get('FIREFOX_BIN')
        self.driver_path = os.environ.get('GECKODRIVER_PATH')