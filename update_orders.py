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


def check_order_open_close(out_df, x, o_now, o_buy):

    delta1441 = out_df.at[x, const.avg1441_col_name] - out_df.at[x-1, const.avg1441_col_name]
    delta181 = out_df.at[x, const.avg181_col_name] - out_df.at[x-1, const.avg181_col_name]
    delta31 = out_df.at[x, const.avg31_col_name] - out_df.at[x-1, const.avg31_col_name]
    delta7 = out_df.at[x, const.avg7_col_name] - out_df.at[x-1, const.avg7_col_name]
    dt = round(out_df.at[x, const.dt_col_name])
    price = out_df.at[x, const.value_col_name]

    o_change = False

    if not o_now:
        if delta1441 > 0 and delta181 > 0 and delta31 > 0 and delta7 > 0:
            o_change = True
            o_now = True
            o_buy = True

        if delta1441 < 0 and delta181 < 0 and delta31 < 0 and delta7 < 0:
            o_change = True
            o_now = True
            o_buy = False
    else:
        if o_buy:
            if (delta1441 + delta181) < 0:
                o_change = True
                o_now = False
        else:
            if (delta1441 + delta181) > 0:
                o_change = True
                o_now = False

    return o_now, o_buy, o_change


def fill_equation_values(out_df, x, o_now, o_buy, mean_value, min_value, max_value):

    if o_now:
        if o_buy:
            out_df.at[x, const.order_col_name] = max_value
        else:
            out_df.at[x, const.order_col_name] = min_value
    else:
        out_df.at[x, const.order_col_name] = mean_value

    return out_df


def fill_order_values(ord_df, o_open, o_buy, beg_dt, beg_val, end_dt, end_val):

    len = ord_df[const.type_col_name].size
    if o_open:
        pos = len # add new row
    else:
        pos = len - 1 # insert values into last row

    if o_buy:
        ord_df.at[pos,const.type_col_name] = const.order_type_buy
    else:
        ord_df.at[pos,const.type_col_name] = const.order_type_sell

    ord_df.at[pos,const.open_dt_col_name] = beg_dt
    ord_df.at[pos,const.open_price_col_name] = beg_val

    if o_open:
        ord_df.at[pos, const.close_dt_col_name] = 0.0
        ord_df.at[pos, const.close_price_col_name] = 0.0
        ord_df.at[pos, const.delta_price] = 0.0
        ord_df.at[pos, const.delta_price_prc] = 0.0
        ord_df.at[pos, const.profit] = 0.0
        ord_df.at[pos, const.profit_prc] = 0.0
        ord_df.at[pos, const.sum_profit] = 0.0
        ord_df.at[pos, const.sum_profit_prc] = 0.0
    else:
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


def get_curr_prev5_minute_utc():
    curr_datetime = datetime.datetime.now()
    curr_datetime = datetime.datetime(
        curr_datetime.year, curr_datetime.month, curr_datetime.day, curr_datetime.hour, curr_datetime.minute, 0)
    prev_datetime = curr_datetime - datetime.timedelta(minutes=5)
    c_utc = curr_datetime.timestamp()
    p_utc = prev_datetime.timestamp()
    return c_utc, p_utc


def check_for_order_open(ord_df):

    len = ord_df[const.type_col_name].size
    if len <= 0:
        order_now = False
        order_buy = False
        beg_dt = 0.0
        beg_val = 0.0
    else:
        pos = len - 1

        close_dt = ord_df.at[pos, const.close_dt_col_name]
        ord_type = ord_df.at[pos, const.type_col_name]
        if close_dt == 0.0: # last order not closed
            order_now = True
            if ord_type==const.order_type_buy:
                order_buy = True
            else:
                order_buy = False
            beg_dt = ord_df.at[pos, const.open_dt_col_name]
            beg_val = ord_df.at[pos, const.open_price_col_name]
        else:
            order_now = False
            order_buy = False
            beg_dt = 0.0
            beg_val = 0.0

    return order_now, order_buy, beg_dt, beg_val


def update_eq_order(out_df, ord_df):

    out_len = out_df[const.dt_col_name].size
    x = out_len - 1

    curr_min_utc, prev5_min_utc = get_curr_prev5_minute_utc()
    last_dt_utc = out_df.at[x, const.dt_col_name]

    last_dt = datetime.datetime(last_dt_utc)
    curr_min_dt = datetime.datetime(prev5_min_utc)

    print('..[' + last_dt + ',' + curr_min_dt + '].', end='')

    if (last_dt_utc >= prev5_min_utc) & (last_dt_utc <= curr_min_utc):

        ord_change = False
        order_now, order_buy, beg_dt, beg_val = check_for_order_open(ord_df)

        mean_value = out_df[const.value_col_name].mean()
        min_value = out_df[const.value_col_name].min()
        max_value = out_df[const.value_col_name].max()

        out_df.at[0, const.order_col_name] = mean_value
        out_df.at[1, const.order_col_name] = mean_value

        order_now, order_buy, ord_change = check_order_open_close(out_df, x, order_now, order_buy)
        out_df = fill_equation_values(out_df, x, order_now, order_buy, mean_value, min_value, max_value)

        if ord_change:
            if order_now:
                beg_dt = out_df.at[x, const.dt_col_name]
                beg_val = out_df.at[x, const.value_col_name]
                ord_df = fill_order_values(ord_df, order_now, order_buy, beg_dt, beg_val, 0.0, 0.0)
            else:
                end_dt = out_df.at[x, const.dt_col_name]
                end_val = out_df.at[x, const.value_col_name]
                ord_df = fill_order_values(ord_df, order_now, order_buy, beg_dt, beg_val, end_dt, end_val)

    return out_df, ord_df


def update_orders_by_symbol(symbol_str):

    print('Update equations ' + symbol_str + ' ', end='')

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

    eq_df, ord_df = update_eq_order(eq_df, ord_df)
    print('..update ord.', end='')

    ord_df.to_csv(ord_file_name, index=False, header=True)
    print('..save ord.', end='')

    eq_df.to_csv(eq_file_name, index=False, header=True)
    print('..save eq.', end='')

    print('Completed !')


