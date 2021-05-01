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


def client_order_create(side: str, symbol: str, qty: float, price: float, reduce_only:bool):

    order_type:str = const.order_type_market
    time_in_force:str = const.order_time_in_force_good_till_cancel

    if side == const.order_side_buy:
        stop_loss:float = round(price * const.order_stop_lost_koef_buy,4)
    else:
        stop_loss:float = round(price * const.order_stop_lost_koef_sell,4)

    if side == const.order_side_buy:
        take_profit:float = round(price * const.order_take_profit_koef_buy,4)
    else:
        take_profit:float = round(price * const.order_take_profit_koef_sell,4)

    stop_loss_str = str(stop_loss)
    take_profit_str = str(take_profit)

    close_on_trigger:bool = False
    tsms_str = current_time_ms()
    qty_str = str(round(qty, 4))

    req_data = {
        'api_key': const.SERVER_ACCESS_API_KEY,
        'timestamp': tsms_str,
        'side': side,
        'symbol': symbol,
        'order_type': order_type,
        'qty': qty_str,
        'stop_loss': stop_loss_str,
        'reduce_only': reduce_only,
        'close_on_trigger': close_on_trigger,
        'take_profit': take_profit_str,
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
            qty = result['qty']
            return True, order_id, time_now, price, qty

    return False, 0, 0, 0.0, 0.0


def client_order_get_status(order_id: str, symbol: str):

    tsms_str = current_time_ms()
    req_data = {
        'api_key': const.SERVER_ACCESS_API_KEY,
        'timestamp': tsms_str,
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


def client_position_oc(side: str,symbol: str, qty_in_usd: float, price: float, reduce_only:bool):

    qty: float = round(qty_in_usd / price, 4)
    success_create, order_id, time_now, price, qty = \
        client_order_create(side, symbol, qty, price, reduce_only)

    if not success_create:
        return False, '', time_now, qty, qty_in_usd, price

    for t in range(0, 3):
        success_status, order_status = client_order_get_status(order_id, symbol)
        if success_status and order_status == const.order_status_filled:
            break
        time.sleep(0.5)

    if (not success_status) or (order_status != const.order_status_filled):
        return False, '', time_now, qty, qty_in_usd, price

    return True, order_id, time_now, qty, qty_in_usd, price


def client_position_open(side: str, symbol: str, qty_in_usd: float, price: float):
    return client_position_oc(side, symbol, qty_in_usd, price, False)


def client_position_close(side: str, symbol: str, qty_in_usd: float, price: float):

    if side == const.order_side_buy:
        side = const.order_side_sell
    else:
        side = const.order_side_buy

    return client_position_oc(side, symbol, qty_in_usd, price, True)


def client_position_check(side: str, symbol: str):

    tsms_str = current_time_ms()
    req_data = {
        'api_key': const.SERVER_ACCESS_API_KEY,
        'timestamp': tsms_str,
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
            if len(result) < 1:
                return False
            position_data = result[0]
            side_val = position_data['side']
            size = position_data['size']
            if (side_val == side) and (size > 0):
                return True

    return False

