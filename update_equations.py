import os
import json
import requests
import time
import datetime
import numpy as np
import pandas as pd
from pconst import const
from IPython.core.display import display
from matplotlib import pylab

%pylab


const.SUFFIX = 'equations'

const.BTCUSD = 'BTCUSD'
const.ETHUSD = 'ETHUSD'
const.EOSUSD = 'EOSUSD'
const.XRPUSD = 'XRPUSD'

const.avg7_hwnd    = 3
const.avg31_hwnd   = 15
const.avg181_hwnd  = 90
const.avg8641_count = 4320

const.dt_col_name = 'dt'
const.value_col_name = 'value'
const.delta1_col_name = 'delta1'
const.delta2_col_name = 'delta2'
const.avg7_col_name = 'avg7'
const.avg31_col_name = 'avg31'
const.avg181_col_name = 'avg181'
const.avg8641_col_name = 'avg8641'


def get_cache_filename(symbol_str):
    return r'data/' + symbol_str.lower() + '.csv'


def get_output_filename(symbol_str):
    return r'data/' + symbol_str.lower() + '_' + const.SUFFIX + '.csv'


def update_eq_value(in_df):

    out_df = pd.DataFrame(columns=[const.dt_col_name, const.value_col_name, const.delta1_col_name,
                                   const.delta2_col_name, const.avg7_col_name, const.avg31_col_name,
                                   const.avg181_col_name, const.avg8641_col_name])

    for index, item in in_df.iterrows():
        new_value = ( item['open'] + item['close'] ) / 2.0
        new_row = {
            const.dt_col_name: item[const.dt_col_name],
            const.value_col_name: new_value,
            const.delta1_col_name: 0,
            const.delta2_col_name: 0,
            const.avg7_col_name: 0,
            const.avg31_col_name: 0,
            const.avg181_col_name: 0,
            const.avg8641_col_name: 0
        }
        out_df = out_df.append(new_row, ignore_index=True)

    return out_df


def update_eq_delta1(out_df):

    lenght = out_df[const.dt_col_name].size
    out_df.at[0,const.delta1_col_name] = 0.0

    for x in range(1, lenght):
        out_df.at[x, const.delta1_col_name] = out_df.at[x, const.value_col_name] - out_df.at[x-1, const.value_col_name]

    return out_df


def update_eq_delta2(out_df):

    lenght = out_df[const.dt_col_name].size
    out_df.at[0,const.delta2_col_name] = 0.0
    out_df.at[1,const.delta2_col_name] = 0.0

    for x in range(2, lenght):
        out_df.at[x, const.delta2_col_name] = out_df.at[x, const.delta1_col_name] - out_df.at[x-1, const.delta1_col_name]

    return out_df


def calc_avg_value(out_df, index, hwnd_size, full_length):
    sumv = 0.0
    count = hwnd_size*2 + 1

    start_idx = index - hwnd_size
    if start_idx<0.0:
        start_idx = 0.0

    end_idx = index + hwnd_size + 1
    if end_idx>full_length:
        end_idx = full_length

    for x in range(start_idx, end_idx):
        sumv += out_df.at[x, const.value_col_name]
    return sumv / count


def update_eq_avg(out_df, hwnd_size, col_name):

    ln = out_df[const.dt_col_name].size

    for x in range(0, ln):
        out_df.at[x, col_name] = calc_avg_value(out_df, x, hwnd_size, ln)

    return out_df


def update_equations(symbol_str):

    in_file_name = get_cache_filename(symbol_str)
    in_df = pd.read_csv(in_file_name)
    print('.', end='')

    out_df = update_eq_value(in_df)
    print('.', end='')

    out_df = update_eq_delta1(out_df)
    print('.', end='')

    out_df = update_eq_delta2(out_df)
    print('.', end='')

    out_df = update_eq_avg(out_df, const.avg7_hwnd)
    print('.', end='')

    out_df = update_eq_avg(out_df, const.avg31_hwnd)
    print('.', end='')

    out_df = update_eq_avg(out_df, const.avg181_hwnd)
    print('.', end='')

    out_df = update_eq_avg(out_df, const.avg8641_count)
    print('.', end='')

    out_file_name = get_output_filename(symbol_str)
    out_df.to_csv(out_file_name, index=False, header=True)
    print('.')


print( ' Full update equations for data from cache *.csv --------------------------------------')

print('BTCUSD calculating', end='')
update_equations(const.BTCUSD)

print('ETHUSD calculating', end='')
update_equations(const.ETHUSD)

print('EOSUSD calculating', end='')
update_equations(const.EOSUSD)

print('XRPUSD calculating', end='')
update_equations(const.XRPUSD)

print( ' See result in /data/*_equations.csv --------------------------------------------------')
