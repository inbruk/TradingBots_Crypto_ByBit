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


def prepare_1441_4_chart(df):

    min = df[const.avg1441_col_name].min()
    max = df[const.avg1441_col_name].max()
    mid = (max-min)/2.0
    len = df[const.avg1441_col_name].size

    for x in range(0, len):
        val = df.at[x, const.avg1441_col_name] - min - mid
        df.at[x, const.avg1441_col_name] = val

    return df


def draw_one_symbol(symbol_str, start_dt, end_dt):

    in_file_name = get_equs_filename(symbol_str)
    df = pd.read_csv(in_file_name)
    # display(df)
    print('...loaded.', end='')

    df = prepare_1441_4_chart(df)
    print('..prepared.', end='')

    df = df[(df.dt >= start_dt) & (df.dt <= end_dt)]
    print('..filtered.', end='')

    fig, axes = plt.subplots(2, 1)

    axes[0].plot(df[const.dt_col_name], df[const.value_col_name],
                 df[const.dt_col_name], df[const.order_col_name])
    axes[0].set_title('Price and order')

    axes[1].plot(df[const.dt_col_name], df[const.avg1441_col_name],
                 df[const.dt_col_name], df[const.avg181_col_name],
                 df[const.dt_col_name], df[const.avg31_col_name],
                 df[const.dt_col_name], df[const.avg7_col_name])
    axes[1].set_title('avg1441, avg181, avg31, avg7')

    plt.show()
    print('..drawed !')


curr_symbol = const.XTZUSDT
start_dt_utc = 1618174101
end_dt_utc = 1618778973
draw_one_symbol(curr_symbol, start_dt_utc, end_dt_utc)



