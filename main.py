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
from select_best_cur import *


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


update_orders = True
currencies = [
    const.SUSHIUSDT,
    const.ETHUSDT,
    const.XRPUSDT,
    const.UNIUSDT
]

while 1 == 1:
    next_utc = get_next_minute_utc()

    for symbol in currencies:  # const.CURRENCIES:
        get_values_and_update_cache(symbol)
        update_equations_by_symbol(symbol)
        if update_orders:
            update_orders_by_symbol(symbol, const.one_curr_order_amount)
        else:
            fill_orders_by_historical_data(symbol)
        print()

    if not update_orders:
        break

    curr_utc = get_curr_minute_utc()
    while curr_utc < next_utc:
        curr_utc = get_curr_minute_utc()




