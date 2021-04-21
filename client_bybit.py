import os
import json
import requests
import time
import datetime
import pandas as pd
from pconst import const
from consts import *
from IPython.core.display import display


const.PUBLIC_API_URL = 'https://api.bybit.com/public/linear/'

const.SERVER_ACCESS_NAME = os.getenv('BYBIT_NAME')
const.SERVER_ACCESS_API_KEY = os.getenv('BYBIT_API_KEY')
const.SERVER_ACCESS_SECRET_CODE = os.getenv('BYBIT_SECRET_CODE')


def client_load_hour_prices(symbol_str, begin_utc):

    begin_utc_int = round(begin_utc)

    req = requests.get(
        const.PUBLIC_API_URL + 'kline',
        {
            'symbol':symbol_str,
            'interval':1,
            'from':begin_utc_int,
            'limit':60
        }
    )

    if req.ok:
        df = pd.DataFrame(columns=['dt', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
        json_data = json.loads(req.text)
        json_rows = json_data['result']
        for item in json_rows:
            dt = round(item['open_time'])
            new_row = { 'dt':dt, 'open':item['open'], 'high':item['high'], 'low':item['low'],
                        'close':item['close'], 'volume':item['volume'], 'turnover':item['turnover']  }
            df = df.append(new_row, ignore_index=True)

    return df


def client_create_order():


def client_read_order(order_id):


def client_update_order(order_id):


def client_close_order(order_id):


