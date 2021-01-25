import os
import json
import requests
import datetime
import pandas as pd
from IPython.core.display import display

public_api_url = 'https://api.bybit.com/v2/public/'

server_access_name = os.getenv('BYBIT_NAME')
server_access_api_key = os.getenv('BYBIT_API_KEY')
server_access_secret_code = os.getenv('BYBIT_SECRET_CODE')

# display(server_access_name)
# display(server_access_api_key)
# display(server_access_secret_code)


def load_hour_values(symbol_str, begin_utc):

    req = requests.get(
        public_api_url + 'kline/list',
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


def merge_and_save_to_cache(symbol_str, new_df):

    df = pd.DataFrame(columns=['dt', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
    filename = r'data/' + symbol_str.lower() + '.csv'

    # if exists load cached data
    if os.path.exists(filename):
       df = pd.read_csv(filename)

    # insert new data and remove doubles by dt
    df = df.append(new_df, ignore_index=True)
    df.drop_duplicates(subset='dt', keep='first', inplace=True)

    df.to_csv(filename, index = False, header=True)

    return df


print( '--------------------------------------')
new_df = load_hour_values('BTCUSD',1607648220)
res_df = merge_and_save_to_cache('BTCUSD', new_df)
display(res_df)


print( '--------------------------------------')
curr_datetime = datetime.datetime.now()
display(curr_datetime)

curr_datetime += datetime.timedelta(hours=1)
display(curr_datetime)


curr_timestamp = curr_datetime.timestamp()
display(curr_timestamp)

