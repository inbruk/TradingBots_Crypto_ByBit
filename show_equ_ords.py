import os
import json
import requests
import time
import datetime
import pandas as pd
from pconst import const
from consts import *
from IPython.core.display import display
import matplotlib.pyplot as plt


def get_equs_filename(symbol_str):
    return r'data/' + symbol_str.lower() + '_' + const.SUFFIX + '.csv'


def get_orders_filename(symbol_str):
    return r'data/' + symbol_str.lower() + '_' + const.ORDERS + '.csv'


def prepare_1441_4_chart(df):

    min = df[const.avg_slow_col_name].min()
    max = df[const.avg_slow_col_name].max()
    mid = (max-min)/2.0
    len = df[const.avg_slow_col_name].size

    for x in range(0, len):
        val = df.at[x, const.avg_slow_col_name] - min - mid
        df.at[x, const.avg_slow_col_name] = val

    return df


def fill_order_values(eq_df, symbol_str):

    ord_file_name = get_orders_filename(symbol_str)
    if os.path.exists(ord_file_name):
        ord_df = pd.read_csv(ord_file_name)
    else:
        raise Exception('Order file is not found !!!')

    mean_value = eq_df[const.value_col_name].mean()
    min_value = eq_df[const.value_col_name].min()
    max_value = eq_df[const.value_col_name].max()

    eq_len = eq_df[const.dt_col_name].size
    for x in range(0, eq_len):
        eq_df.at[x, const.order_col_name] = mean_value

    ord_len = ord_df[const.type_col_name].size
    for pos in range(0, ord_len):
        if ord_df.at[pos, const.close_dt_col_name] != 0.0:
            side = ord_df.at[pos, const.type_col_name]
            beg_dt = ord_df.at[pos, const.open_dt_col_name]
            #  beg_val = ord_df.at[pos, const.open_price_col_name]
            end_dt = ord_df.at[pos, const.close_dt_col_name]
            #  end_val = ord_df.at[pos, const.close_price_col_name]
            for x in range(0, eq_len):
                curr_dt = eq_df.at[x, const.dt_col_name]
                if beg_dt <= curr_dt <= end_dt:
                    if side == const.order_side_buy:
                        eq_df.at[x, const.order_col_name] = max_value
                    else:
                        eq_df.at[x, const.order_col_name] = min_value

    return eq_df


def draw_one_symbol(symbol_str, start_dt):

    in_file_name = get_equs_filename(symbol_str)
    df = pd.read_csv(in_file_name)
    # display(df)
    print('...loaded.', end='')

    if update_orders:
        df = fill_order_values(df, symbol_str)
        print('...fill order values.', end='')

#    df = prepare_1441_4_chart(df)
    print('..prepared.', end='')

    df = df[df.dt >= start_dt]
    print('..filtered.', end='')

    fig, axes = plt.subplots(2, 1)

    axes[0].plot(df[const.dt_col_name], df[const.value_col_name],
                 # df[const.dt_col_name], df[const.avg6_col_name],
                 # df[const.dt_col_name], df[const.avg1_col_name],
                 # df[const.dt_col_name], df[const.avg8_col_name],
                 df[const.dt_col_name], df[const.avg_fast_col_name],
                 df[const.dt_col_name], df[const.avg_slow_col_name],
                 df[const.dt_col_name], df[const.order_col_name],
                 )
    axes[0].set_title('Price')

    axes[1].plot(
                 df[const.dt_col_name], df[const.value_col_name],
                 # df[const.dt_col_name], df[const.avg_fast_col_name],
                 # df[const.dt_col_name], df[const.avg_slow_col_name],
                 df[const.dt_col_name], df[const.avg1_col_name],
                 df[const.dt_col_name], df[const.avg2_col_name],
                 df[const.dt_col_name], df[const.avg3_col_name],
                 # df[const.dt_col_name], df[const.avg4_col_name],
                 # df[const.dt_col_name], df[const.avg5_col_name],
                 # df[const.dt_col_name], df[const.avg6_col_name],
                 # df[const.dt_col_name], df[const.avg7_col_name],
                 # df[const.dt_col_name], df[const.avg8_col_name],
    )
    axes[1].set_title('avg1441, avg181p, avg31p, avg7p')

    plt.show()
    print('..drawed !')


update_orders = False

# curr_symbol = const.BTCUSDT
# curr_symbol = const.AAVEUSDT
# curr_symbol = const.ADAUSDT
# curr_symbol = const.AVAXUSDT
# curr_symbol = const.BCHUSDT
# curr_symbol = const.BNBUSDT
# curr_symbol = const.BTCUSDT
# curr_symbol = const.DOGEUSDT
# curr_symbol = const.DOTUSDT
curr_symbol = const.ETHUSDT
# curr_symbol = const.LINKUSDT
# curr_symbol = const.LTCUSDT
# curr_symbol = const.SOLUSDT
# curr_symbol = const.SUSHIUSDT
# curr_symbol = const.TRXUSDT
# curr_symbol = const.XRPUSDT
# curr_symbol = const.XEMUSDT
# curr_symbol = const.XTZUSDT
# curr_symbol = const.UNIUSDT
# curr_symbol = const.SUSHIUSDT

start_dt_utc = const.START_UTC
draw_one_symbol(curr_symbol, start_dt_utc)



