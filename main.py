import os
import json
import requests
import time
import datetime
import pandas as pd
from pconst import const
from consts import *
from IPython.core.display import display
from update_candles import *
from update_equations import *
from update_orders import *


def get_curr_minute_utc():
    curr_datetime = datetime.datetime.now()
    curr_datetime = datetime.datetime(
        curr_datetime.year, curr_datetime.month, curr_datetime.day, curr_datetime.hour, curr_datetime.minute, 0)
    c_utc = curr_datetime.timestamp()
    return c_utc


def get_next_minute_utc():
    curr_datetime = datetime.datetime.now()
    curr_datetime = datetime.datetime(
        curr_datetime.year, curr_datetime.month, curr_datetime.day, curr_datetime.hour, curr_datetime.minute, 0)
    next_datetime = curr_datetime + datetime.timedelta(minutes=1)
    n_utc = next_datetime.timestamp()
    return n_utc


while True:

    next_utc = get_next_minute_utc()

    update_candles()
    update_equations()
    update_orders()

    curr_utc = get_curr_minute_utc()

    while curr_utc < next_utc:
        time.sleep(1)
        curr_utc = get_curr_minute_utc()




