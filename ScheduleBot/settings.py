import os


class Settings:

    def __init__(self):

        self.init_time_settings()
        self.init_channels_settings()

    def init_time_settings(self):

        self.hour = 60*60

        self.weekday = {'mon' : 0, 'tue' : 1 , 'wed' : 2,
                        'thu' : 3, 'fri' : 4, 'sat' : 5, 'sun' : 6}

    def init_channels_settings(self):

        self.channels = {}
        self.channels['iot20'] = int(os.getenv('CHANNEL_IOT20'))
        self.channels['iot'] = int(os.getenv('CHANNEL_IOT'))