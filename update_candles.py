import os
import json
import requests
import time
import datetime
import pandas as pd
from pconst import const
from consts import *
from IPython.core.display import display


def load_hour_values_from_server(symbol_str, begin_utc):

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


def get_cache_filename(symbol_str):
    return r'data/' + symbol_str.lower() + '.csv'


def load_values_from_cache(symbol_str):

    df = pd.DataFrame(columns=['dt', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
    filename = get_cache_filename(symbol_str)

    if os.path.exists(filename):
       df = pd.read_csv(filename)

    return df


def get_prev_minute_utc():
    curr_datetime = datetime.datetime.now()
    curr_datetime = datetime.datetime(curr_datetime.year, curr_datetime.month, curr_datetime.day, curr_datetime.hour, curr_datetime.minute, 0)
    curr_datetime -= datetime.timedelta(minutes=1)
    curr_utc = curr_datetime.timestamp()
    return curr_utc


def get_values_and_update_cache(symbol_str):

    print('Loaded to cache ' + symbol_str + ' ...', end='')

    df = load_values_from_cache(symbol_str)
    if len(df) > 0:
        current_start_utc = round(df['dt'].max())
    else:
       current_start_utc = const.START_UTC

    curr_utc = get_prev_minute_utc()
    while True:
        time.sleep(0.1)
        new_df = load_hour_values_from_server(symbol_str, current_start_utc)
        df = df.append(new_df, ignore_index=True)
        df.drop_duplicates(subset='dt', keep='first', inplace=True)
        current_end_utc = round(df['dt'].max())
        if current_end_utc >= curr_utc:
            break
        else:
            current_start_utc = round(current_end_utc)

    filename = get_cache_filename(symbol_str)
    df.to_csv(filename, index=False, header=True)

    print(' Complete!')





