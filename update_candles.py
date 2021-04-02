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

    req = requests.get(
        const.PUBLIC_API_URL + 'kline',
        {
            'symbol':symbol_str,
            'interval':1,
            'from':begin_utc,
            'limit':60
        }
    )

    if req.ok:
        df = pd.DataFrame(columns=['dt', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
        json_data = json.loads(req.text)
        json_rows = json_data['result']
        for item in json_rows:
            new_row = { 'dt':item['open_time'], 'open':item['open'], 'high':item['high'], 'low':item['low'],
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

    df = load_values_from_cache(symbol_str)
    if len(df) > 0:
        current_start_utc = df['dt'].max()
    else:
       current_start_utc = const.START_UTC

    curr_utc = get_prev_minute_utc()
    while True:
        time.sleep(1)
        new_df = load_hour_values_from_server(symbol_str, current_start_utc)
        df = df.append(new_df, ignore_index=True)
        df.drop_duplicates(subset='dt', keep='first', inplace=True)
        current_end_utc = df['dt'].max()
        if current_end_utc >= curr_utc:
            break
        else:
            current_start_utc = round(current_end_utc)

    filename = get_cache_filename(symbol_str)
    df.to_csv(filename, index=False, header=True)
    return df


def update_candles():

    print( ' UPDATE CANDLES ------------------------------------------------------------------START')
    print( ' Load data from Bybit and store to cache *.csv ')
    print( ' Work until -1 minute from now ')

    print('BTCUSDT loading...')
    res_df = get_values_and_update_cache(const.BTCUSDT)
    print('BTCUSDT data in cache ' + str(len(res_df)))

    print('BCHUSDT loading...')
    res_df = get_values_and_update_cache(const.BCHUSDT)
    print('BCHUSDT data in cache ' + str(len(res_df)))

    print('ETHUSDT loading...')
    res_df = get_values_and_update_cache(const.ETHUSDT)
    print('ETHUSDT data in cache ' + str(len(res_df)))

    print('LTCUSDT loading...')
    res_df = get_values_and_update_cache(const.LTCUSDT)
    print('LTCUSDT data in cache ' + str(len(res_df)))

    print('LINKUSDT loading...')
    res_df = get_values_and_update_cache(const.LINKUSDT)
    print('LINKUSDT data in cache ' + str(len(res_df)))

    print('XTZUSDT loading...')
    res_df = get_values_and_update_cache(const.XTZUSDT)
    print('XTZUSDT data in cache ' + str(len(res_df)))

    print('ADAUSDT loading...')
    res_df = get_values_and_update_cache(const.ADAUSDT)
    print('ADAUSDT data in cache ' + str(len(res_df)))

    print('DOTUSDT loading...')
    res_df = get_values_and_update_cache(const.DOTUSDT)
    print('DOTUSDT data in cache ' + str(len(res_df)))

    print('UNIUSDT loading...')
    res_df = get_values_and_update_cache(const.UNIUSDT)
    print('UNIUSDT data in cache ' + str(len(res_df)))

    print( ' See result in /data/*.csv')
    print( ' UPDATE CANDLES ------------------------------------------------------------------STOP')


