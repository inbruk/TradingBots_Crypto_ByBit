import os
import json
import requests
import hashlib
import hmac
import time
import datetime
import pandas as pd
from pconst import const
from consts import *
from IPython.core.display import display


const.COMMON_API_URL = 'https://api.bybit.com/'

const.PUBLIC_API_ORDER = const.COMMON_API_URL + 'public/linear/'
const.PUBLIC_API_ORDER_KLINE = const.PUBLIC_API_ORDER + 'kline'

const.PRIVATE_API_ORDER = const.COMMON_API_URL + 'private/linear/order/'
const.PRIVATE_API_ORDER_CREATE = const.PRIVATE_API_ORDER + 'create'
const.PRIVATE_API_ORDER_LIST = const.PRIVATE_API_ORDER + 'list'

const.PRIVATE_API_POSITION = const.COMMON_API_URL + 'private/linear/position/'
const.PRIVATE_API_POSITION_LIST = const.PRIVATE_API_POSITION + 'list'

const.SERVER_ACCESS_NAME = os.getenv('BYBIT_NAME')
const.SERVER_ACCESS_API_KEY = os.getenv('BYBIT_API_KEY')
const.SERVER_ACCESS_SECRET_CODE = os.getenv('BYBIT_SECRET_CODE')


def client_load_hour_prices(symbol_str, begin_utc):

    begin_utc_int = round(begin_utc)

    req = requests.get(
        const.PUBLIC_API_KLINE,
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


def client_calculate_sign(params):
    params_str = ''
    for key in sorted(params.keys()):
        v = params[key]
        if isinstance(params[key], bool):
            if params[key]:
                v = 'true'
            else :
                v = 'false'
        params_str += key + '=' + str(v) + '&'
    params_str = params_str[:-1]
    params_bytes = params_str.encode("utf-8")
    key_bytes = const.SERVER_ACCESS_SECRET_CODE.encode("utf-8")
    params_hash = hmac.new(key_bytes, params_bytes, hashlib.sha256)
    params_sign = params_hash.hexdigest()

    return params_sign


def current_time_ms():
    res = str(int(time.time() * 1000))
    return res


def client_order_create(side: str, symbol: str, qty: int, price: float):

    order_type:str = const.order_type_market
    time_in_force:str = const.order_time_in_force_good_till_cancel
    # qty:float = qty_in_usd / price

    # if side == const.order_side_buy:
    #     stop_loss:float = price * const.order_stop_lost_koef_buy
    # else:
    #     stop_loss:float = price * const.order_stop_lost_koef_sell
    #
    # if side == const.order_side_buy:
    #     take_profit:float = price * const.order_take_profit_koef_buy
    # else:
    #     take_profit:float = price * const.order_take_profit_koef_sell

    reduce_only:bool = False
    close_on_trigger:bool = False
    tsms_str = current_time_ms

    req_data = {
        'api_key': const.SERVER_ACCESS_API_KEY,
        'timestamp': tsms_str,
        'side': side,
        'symbol': symbol,
        'order_type': order_type,
        'qty': qty,
      #  'stop_loss': stop_loss,
        'reduce_only': reduce_only,
        'close_on_trigger': close_on_trigger,
      #  'take_profit': take_profit,
        'time_in_force': time_in_force,
    }

    sign = client_calculate_sign(req_data)
    req_data['sign'] = sign

    req = requests.post(const.PRIVATE_API_ORDER_CREATE, json=req_data)

    if req.ok:
        json_data = json.loads(req.text)
        ret_code = json_data['ret_code']
        if ret_code == 0:
            time_now = json_data['time_now']
            result = json_data['result']
            order_id = result['order_id']
            price = result['price']
            qty_in_usd = result['qty_in_usd']
            return True, order_id, time_now, price, qty_in_usd

    return False, 0, 0, 0.0, 0.0


def client_order_get_status(order_id: str, symbol: str):

    req_data = {
        'api_key': const.SERVER_ACCESS_API_KEY,
        'timestamp': datetime.datetime.now().timestamp(),
        'order_id': order_id,
        'symbol': symbol
    }

    sign = client_calculate_sign(req_data)
    req_data['sign'] = sign

    req = requests.get(const.PRIVATE_API_ORDER_LIST, params=req_data)

    if req.ok:
        json_data = json.loads(req.text)
        ret_code = json_data['ret_code']
        if ret_code == 0:
            result = json_data['result']
            order_data = result['data'][0]
            order_status = order_data['order_status']
            return True, order_status

    return False, const.order_status_rejected


def client_position_read(symbol: str):

    req_data = {
        'api_key': const.SERVER_ACCESS_API_KEY,
        'timestamp': datetime.datetime.now().timestamp(),
        'symbol': symbol
    }

    sign = client_calculate_sign(req_data)
    req_data['sign'] = sign

    req = requests.get(const.PRIVATE_API_POSITION_LIST, params=req_data)

    if req.ok:
        json_data = json.loads(req.text)
        ret_code = json_data['ret_code']
        if ret_code == 0:
            result = json_data['result']
            position_data = result['data'][0]
            side = position_data['side']
            size = position_data['size']
            position_value = position_data['position_value']
            entry_price = position_data['entry_price']
            return True, side, size, position_value, entry_price

    return False, '', float, float, float
