from datetime import datetime as time
import pytz


def get_cur_hour() -> int : 
    """returns current hour as an int"""
    return time.now(pytz.timezone('Europe/Stockholm')).hour


def get_cur_weekday() -> int :
    """returns current weekday as an int 0-6"""
    return time.today().weekday()


def get_cur_week() -> int :
    """returns current week as an int"""
    return time.today().isocalendar()[1]