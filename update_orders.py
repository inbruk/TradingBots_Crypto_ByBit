import os
import json
import requests
import time
import datetime
import pandas as pd
from pconst import const
from consts import *
from IPython.core.display import display


def get_equations_filename(symbol_str):
    return r'data/' + symbol_str.lower() + '_' + const.SUFFIX + '.csv'


def get_orders_filename(symbol_str):
    return r'data/' + symbol_str.lower() + '_' + const.ORDERS + '.csv'


def check_order_open_close(out_df, x, o_now, o_buy, o_open, o_change):

    delta1441 = out_df.at[x, const.avg1441_col_name] - out_df.at[x-1, const.avg1441_col_name]
    delta181 = out_df.at[x, const.avg181_col_name] - out_df.at[x-1, const.avg181_col_name]
    delta31 = out_df.at[x, const.avg31_col_name] - out_df.at[x-1, const.avg31_col_name]
    delta7 = out_df.at[x, const.avg7_col_name] - out_df.at[x-1, const.avg7_col_name]
    dt = round(out_df.at[x, const.dt_col_name])
    price = out_df.at[x, const.value_col_name]

    o_change = False
    o_open = False

    if not o_now:
        if delta1441 > 0 and delta181 > 0 and delta31 > 0 and delta7 > 0:
            o_change = True
            o_open = True
            o_now = True
            o_buy = True

        if delta1441 < 0 and delta181 < 0 and delta31 < 0 and delta7 < 0:
            o_change = True
            o_open = True
            o_now = True
            o_buy = False
    else:
        if o_buy:
            if (delta1441 + delta181) < 0:
                o_change = True
                o_open = False
                o_now = False
        else:
            if (delta1441 + delta181) > 0:
                o_change = True
                o_open = False
                o_now = False

    return o_now, o_buy, o_open, o_change


def fill_equation_values(out_df, x, o_now, o_buy, mean_value, min_value, max_value):

    if o_now:
        if o_buy:
            out_df.at[x, const.order_col_name] = max_value
        else:
            out_df.at[x, const.order_col_name] = min_value
    else:
        out_df.at[x, const.order_col_name] = mean_value

    return out_df


def fill_order_values(ord_df, o_buy, beg_dt, beg_val, end_dt, end_val):

    len = ord_df[const.type_col_name].size
    pos = len

    if o_buy:
        ord_df.at[pos,const.type_col_name] = const.order_type_buy
    else:
        ord_df.at[pos,const.type_col_name] = const.order_type_sell

    ord_df.at[pos,const.open_dt_col_name] = beg_dt
    ord_df.at[pos,const.open_price_col_name] = beg_val
    ord_df.at[pos,const.close_dt_col_name] = end_dt
    ord_df.at[pos,const.close_price_col_name] = end_val


    if o_buy:
        d_price = end_val - beg_val
    else:
        d_price = beg_val - end_val

    d_price_prc = (d_price/beg_val)*100.0
    p_prc = d_price_prc - 0.4
    p = (p_prc/100.0)*beg_val

    ord_df.at[pos,const.delta_price] = d_price
    ord_df.at[pos,const.delta_price_prc] = d_price_prc
    ord_df.at[pos,const.profit] = p
    ord_df.at[pos,const.profit_prc] = p_prc

    prev = pos - 1
    if prev >= 0:
        ord_df.at[pos, const.sum_profit] = ord_df.at[prev, const.sum_profit] + p
        ord_df.at[pos, const.sum_profit_prc] = ord_df.at[prev, const.sum_profit_prc] + p_prc
    else:
        ord_df.at[pos, const.sum_profit] = p
        ord_df.at[pos, const.sum_profit_prc] = p_prc

    return ord_df


def get_curr_prev_minute_utc():
    curr_datetime = datetime.datetime.now()
    curr_datetime = datetime.datetime(
        curr_datetime.year, curr_datetime.month, curr_datetime.day, curr_datetime.hour, curr_datetime.minute, 0)
    prev_datetime = curr_datetime - datetime.timedelta(minutes=1)
    c_utc = curr_datetime.timestamp()
    p_utc = prev_datetime.timestamp()
    return c_utc, p_utc


def update_eq_order(out_df, ord_df):

    out_len = out_df[const.dt_col_name].size
    x = out_len - 1

    curr_min_utc, prev_min_utc = get_curr_prev_minute_utc()
    last_dt_utc = out_df.at[x, const.dt_col_name]

    if (last_dt_utc >= prev_min_utc) & (last_dt_utc <= curr_min_utc):

        order_now = False
        ord_open = False
        order_buy = True
        ord_change = False

        mean_value = out_df[const.value_col_name].mean()
        min_value = out_df[const.value_col_name].min()
        max_value = out_df[const.value_col_name].max()

        out_df.at[0, const.order_col_name] = mean_value
        out_df.at[1, const.order_col_name] = mean_value

        beg_dt = 0.0
        beg_val = 0.0

        order_now, order_buy, ord_open, ord_change = check_order_open_close(
            out_df, x, order_now, order_buy, ord_open, ord_change)

        out_df = fill_equation_values(out_df, x, order_now, order_buy, mean_value, min_value, max_value)

        if ord_change:
            if ord_open:
                beg_dt = out_df.at[x, const.dt_col_name]
                beg_val = out_df.at[x, const.value_col_name]
            else:
                end_dt = out_df.at[x, const.dt_col_name]
                end_val = out_df.at[x, const.value_col_name]
                ord_df = fill_order_values(ord_df, order_buy, beg_dt, beg_val, end_dt, end_val)

    return out_df


def update_orders_by_symbol(symbol_str):

    eq_file_name = get_equations_filename(symbol_str)
    eq_df = pd.read_csv(eq_file_name)
    print('..load eq.', end='')

    ord_file_name = get_orders_filename(symbol_str)
    if os.path.exists(ord_file_name):
        ord_df = pd.read_csv(ord_file_name)
    else:
        ord_df = pd.DataFrame(columns=[const.type_col_name, const.open_dt_col_name, const.open_price_col_name,
                                       const.close_dt_col_name, const.close_price_col_name,
                                       const.delta_price, const.delta_price_prc, const.profit, const.profit_prc,
                                       const.sum_profit, const.sum_profit_prc])
    print('..load ord.', end='')

    update_eq_order(eq_df, ord_df)
    print('..update ord.', end='')

    ord_df.to_csv(ord_file_name, index=False, header=True)
    print('..save ord.')

    eq_df.to_csv(eq_file_name, index=False, header=True)
    print('..save eq !')


def update_orders():

    print( ' UPDATE EQUATIONS ------------------------------------------------------------------START')
    print( ' Full update equations for data from cache *.csv ')

    print('BTCUSDT calculating', end='')
    update_orders_by_symbol(const.BTCUSDT)

    print('BCHUSDT calculating', end='')
    update_orders_by_symbol(const.BCHUSDT)

    print('ETHUSDT calculating', end='')
    update_orders_by_symbol(const.ETHUSDT)

    print('LTCUSDT calculating', end='')
    update_orders_by_symbol(const.LTCUSDT)

    print('LINKUSDT calculating', end='')
    update_orders_by_symbol(const.LINKUSDT)

    print('XTZUSDT calculating', end='')
    update_orders_by_symbol(const.XTZUSDT)

    print('ADAUSDT calculating', end='')
    update_orders_by_symbol(const.ADAUSDT)

    print('DOTUSDT calculating', end='')
    update_orders_by_symbol(const.DOTUSDT)

    print('UNIUSDT calculating', end='')
    update_orders_by_symbol(const.UNIUSDT)

    print( ' See result in /data/*_orders.csv ')
    print(' UPDATE EQUATIONS ------------------------------------------------------------------STOP')
