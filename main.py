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
        df = pd.DataFrame()
        json_data = json.loads(req.text)
        json_rows = json_data['result']
        for item in json_rows:
            new_row = { 'dt':item['open_time'], 'open':item['open'], 'high':item['high'], 'low':item['low'],
                        'close':item['close'], 'volume':item['volume'], 'turnover':item['turnover']  }
            df = df.append(new_row, ignore_index=True)

    return df

def save_values_to_storage(symbol_str, begin_utc):

    filename = '/data/'



print( '--------------------------------------')
dt = load_hour_values('BTCUSD',1611360000)
display(dt)


print( '--------------------------------------')
curr_datetime = datetime.datetime.now()
display(curr_datetime)

curr_datetime += datetime.timedelta(hours=1)
display(curr_datetime)


curr_timestamp = curr_datetime.timestamp()
display(curr_timestamp)

