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


while 1 == 1:

    next_utc = get_next_minute_utc()

    get_values_and_update_cache(const.ADAUSDT)
    update_equations_by_symbol(const.ADAUSDT)
    update_orders_by_symbol(const.ADAUSDT, 15.0)
    print()

    get_values_and_update_cache(const.DOTUSDT)
    update_equations_by_symbol(const.DOTUSDT)
    update_orders_by_symbol(const.DOTUSDT, 15.0)
    print()

    get_values_and_update_cache(const.BCHUSDT)
    update_equations_by_symbol(const.BCHUSDT)
    update_orders_by_symbol(const.BCHUSDT, 45.0)
    print()

    get_values_and_update_cache(const.LINKUSDT)
    update_equations_by_symbol(const.LINKUSDT)
    update_orders_by_symbol(const.LINKUSDT, 20.0)
    print()

    get_values_and_update_cache(const.ETHUSDT)
    update_equations_by_symbol(const.ETHUSDT)
    update_orders_by_symbol(const.ETHUSDT, 55.0)
    print()

    get_values_and_update_cache(const.XTZUSDT)
    update_equations_by_symbol(const.XTZUSDT)
    update_orders_by_symbol(const.XTZUSDT, 15.0)
    print()

    get_values_and_update_cache(const.UNIUSDT)
    update_equations_by_symbol(const.UNIUSDT)
    update_orders_by_symbol(const.UNIUSDT, 20.0)
    print()

    curr_utc = get_curr_minute_utc()

    while curr_utc < next_utc:
        curr_utc = get_curr_minute_utc()




