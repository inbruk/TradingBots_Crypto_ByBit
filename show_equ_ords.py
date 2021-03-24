import os
import json
import requests
import time
import datetime
import pandas as pd
from pconst import const
from IPython.core.display import display
import matplotlib.pyplot as plt

const.SUFFIX = 'equations'

const.BTCUSD = 'BTCUSD'
const.ETHUSD = 'ETHUSD'
const.EOSUSD = 'EOSUSD'
const.XRPUSD = 'XRPUSD'

const.avg7_hwnd = 3
const.avg31_hwnd = 15
const.avg181_hwnd = 90
const.avg1441_hwnd = 720

const.dt_col_name = 'dt'
const.value_col_name = 'value'
const.delta1_col_name = 'delta1'
const.delta2_col_name = 'delta2'

const.avg7_col_name = 'avg7'
const.avg31_col_name = 'avg31'
const.avg181_col_name = 'avg181'
const.avg1441_col_name = 'avg1441'

const.avg7l_col_name = 'avg7l'
const.avg31l_col_name = 'avg31l'
const.avg181l_col_name = 'avg181l'
const.avg1441l_col_name = 'avg1441l'


def get_equs_filename(symbol_str):
    return r'data/' + symbol_str.lower() + '_' + const.SUFFIX + '.csv'


def draw_one_symbol(symbol_str, start_dt, end_dt):

    in_file_name = get_equs_filename(symbol_str)
    df = pd.read_csv(in_file_name)
    display(df)
    print('...loaded.', end='')

    df = df[(df.dt > start_dt) & (df.dt < end_dt)]
    # display(df)
    print('..filtered.', end='')

    fig, axes = plt.subplots(3,1)  # 1, 1, figsize=(12, 4))

    axes[0].plot(df[const.dt_col_name], df[const.value_col_name],
                 df[const.dt_col_name], df[const.avg1441_col_name],
                 df[const.dt_col_name], df[const.avg1441l_col_name])
    axes[0].set_title('Цена,avg1441l,avg1441l')

    axes[1].plot(df[const.dt_col_name], df[const.avg7_col_name],
                 df[const.dt_col_name], df[const.avg31_col_name],
                 df[const.dt_col_name], df[const.avg181_col_name])
    axes[1].set_title('avg7,avg31,avg181')

    axes[2].plot(df[const.dt_col_name], df[const.avg7l_col_name],
                 df[const.dt_col_name], df[const.avg31l_col_name],
                 df[const.dt_col_name], df[const.avg181l_col_name])
    axes[2].set_title('avg7l,avg31l,avg181l')

    # axes[2].plot(df[const.dt_col_name], df[const.delta1_col_name], df[const.dt_col_name], df[const.delta2_col_name])
    # axes[2].set_title('d1,d2')

    plt.show()
    print('..drawed !')


curr_symbol = const.ETHUSD
start_dt_utc = 1616114100
end_dt_utc = 1616373300
draw_one_symbol(curr_symbol, start_dt_utc, end_dt_utc)
