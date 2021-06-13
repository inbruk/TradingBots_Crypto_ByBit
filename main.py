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

    update_orders = False

    next_utc = get_next_minute_utc()

    get_values_and_update_cache(const.BTCUSDT)
    update_equations_by_symbol(const.BTCUSDT)
    print()

    get_values_and_update_cache(const.AAVEUSDT)
    update_equations_by_symbol(const.AAVEUSDT)
    if update_orders:
        update_orders_by_symbol(const.AAVEUSDT, 50.0)
    print()

    get_values_and_update_cache(const.ADAUSDT)
    update_equations_by_symbol(const.ADAUSDT)
    if update_orders:
        update_orders_by_symbol(const.ADAUSDT, 30.0)
    print()

    get_values_and_update_cache(const.BCHUSDT)
    update_equations_by_symbol(const.BCHUSDT)
    if update_orders:
        update_orders_by_symbol(const.BCHUSDT, 50.0)
    print()

    get_values_and_update_cache(const.DOTUSDT)
    update_equations_by_symbol(const.DOTUSDT)
    if update_orders:
        update_orders_by_symbol(const.DOTUSDT, 30.0)
    print()

    get_values_and_update_cache(const.DOGEUSDT)
    update_equations_by_symbol(const.DOGEUSDT)
    if update_orders:
        update_orders_by_symbol(const.DOGEUSDT, 25.0)
    print()

    get_values_and_update_cache(const.ETHUSDT)
    update_equations_by_symbol(const.ETHUSDT)
    if update_orders:
       update_orders_by_symbol(const.ETHUSDT, 50.0)
    print()

    get_values_and_update_cache(const.LTCUSDT)
    update_equations_by_symbol(const.LTCUSDT)
    if update_orders:
        update_orders_by_symbol(const.LTCUSDT, 30.0)
    print()

    get_values_and_update_cache(const.LINKUSDT)
    update_equations_by_symbol(const.LINKUSDT)
    if update_orders:
        update_orders_by_symbol(const.LINKUSDT, 30.0)
    print()

    get_values_and_update_cache(const.SUSHIUSDT)
    update_equations_by_symbol(const.SUSHIUSDT)
    if update_orders:
        update_orders_by_symbol(const.SUSHIUSDT, 30.0)
    print()

    # get_values_and_update_cache(const.XRPUSDT)
    # update_equations_by_symbol(const.XRPUSDT)
    # if update_orders:
    #     update_orders_by_symbol(const.XRPUSDT, 25.0)
    # print()

    # bad results
    # get_values_and_update_cache(const.XEMUSDT)
    # update_equations_by_symbol(const.XEMUSDT)
    # if update_orders:
    #     update_orders_by_symbol(const.XEMUSDT, 25.0)
    # print()

    get_values_and_update_cache(const.XTZUSDT)
    update_equations_by_symbol(const.XTZUSDT)
    if update_orders:
        update_orders_by_symbol(const.XTZUSDT, 30.0)
    print()

    get_values_and_update_cache(const.UNIUSDT)
    update_equations_by_symbol(const.UNIUSDT)
    if update_orders:
        update_orders_by_symbol(const.UNIUSDT, 30.0)
    print()

    curr_utc = get_curr_minute_utc()

    while curr_utc < next_utc:
        curr_utc = get_curr_minute_utc()




