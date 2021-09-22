from datetime import datetime as time
import pytz
from re import match
from argparse import ArgumentTypeError


def get_cur_hour() -> int : 
    """returns current hour as an int"""
    return time.now(pytz.timezone('Europe/Stockholm')).hour


def get_cur_weekday() -> int :
    """returns current weekday as an int 0-6"""
    return time.today().weekday()


def get_cur_week() -> int :
    """returns current week as an int"""
    return time.today().isocalendar()[1]

def date_type(arg_val , pattern = '^([0-9]{1,2}\/[0-9]{1,2})$'):
    
    if match(pattern, arg_val):
        return arg_val
    raise ArgumentTypeError
    
def week_type(arg_val):
    try:
        week = int(arg_val)
        if week < 53 and week >= 0:
            return arg_val
    except:
        raise ArgumentTypeError
     
    raise ArgumentTypeError