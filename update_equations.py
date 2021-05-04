import os
import json
import requests
import time
import datetime
import pandas as pd
from pconst import const
from consts import *
from IPython.core.display import display


def get_cache_filename(symbol_str):
    return r'data/' + symbol_str.lower() + '.csv'


def get_output_filename(symbol_str):
    return r'data/' + symbol_str.lower() + '_' + const.SUFFIX + '.csv'


def update_eq_value(in_df, old_df):
    num_rows = in_df[const.dt_col_name].size
    out_df = pd.DataFrame(index=range(num_rows),
                          columns=[const.dt_col_name, const.value_col_name, const.delta1_col_name,
                                   const.delta2_col_name, const.avg7_col_name, const.avg31_col_name,
                                   const.avg181_col_name, const.avg1441_col_name,
                                   const.avg7p_col_name, const.avg31p_col_name, const.avg181p_col_name,
                                   const.order_col_name])

    for index, item in in_df.iterrows():
        dt = round(item[const.dt_col_name])
        out_df.at[index,const.dt_col_name] = dt
        out_df.at[index,const.value_col_name] = 0.0,
        out_df.at[index,const.delta1_col_name] = 0.0,
        out_df.at[index,const.delta2_col_name] = 0.0,
        out_df.at[index,const.avg7_col_name] = 0.0,
        out_df.at[index,const.avg31_col_name] = 0.0,
        out_df.at[index,const.avg181_col_name] = 0.0,
        out_df.at[index,const.avg1441_col_name] = 0.0,
        out_df.at[index,const.avg7p_col_name] = 0.0,
        out_df.at[index,const.avg31p_col_name] = 0.0,
        out_df.at[index,const.avg181p_col_name] = 0.0,
        out_df.at[index,const.order_col_name] = 0.0

    in_len = in_df[const.dt_col_name].size
    old_len = old_df[const.dt_col_name].size

    for x in range(0, old_len):
        out_df.at[x, const.value_col_name] = old_df.at[x, const.value_col_name]

    for x in range(old_len, in_len):
        out_df.at[x, const.value_col_name] = (in_df.at[x, const.open_col_name] + in_df.at[x, const.close_col_name]) / 2.0

    return out_df


def update_eq_delta1(old_df, out_df):

    out_len = out_df[const.dt_col_name].size
    old_len = old_df[const.dt_col_name].size
    if old_len < 1:
        old_len = 1

    out_df.at[0, const.delta1_col_name] = 0.0

    for x in range(1, old_len):
        out_df.at[x, const.delta1_col_name] = old_df.at[x, const.delta1_col_name]

    for x in range(old_len, out_len):
        out_df.at[x, const.delta1_col_name] = out_df.at[x, const.value_col_name] - out_df.at[x-1, const.value_col_name]

    return out_df


def update_eq_delta2(old_df, out_df):

    out_len = out_df[const.dt_col_name].size
    old_len = old_df[const.dt_col_name].size
    if old_len < 2:
        old_len = 2

    out_df.at[0, const.delta2_col_name] = 0.0
    out_df.at[1, const.delta2_col_name] = 0.0

    for x in range(2, old_len):
        out_df.at[x, const.delta2_col_name] = old_df.at[x, const.delta2_col_name]

    for x in range(old_len, out_len):
        out_df.at[x, const.delta2_col_name] = out_df.at[x, const.delta1_col_name] - out_df.at[x-1, const.delta1_col_name]

    return out_df


def calc_avg_value(out_df, index, hwnd_size, full_length):
    sumv = 0.0

    start_idx = index - hwnd_size
    if start_idx<0:
        start_idx = 0

    end_idx = index + hwnd_size + 1
    if end_idx > full_length:
        end_idx = full_length

    count = 0
    for x in range(start_idx, end_idx):
        sumv += out_df.at[x, const.value_col_name]
        count += 1

    return sumv/count


def smooth_filter(out_df, index, hwnd_size, full_length, col_name):
    sumv = 0.0

    start_idx = index - hwnd_size
    if start_idx<0:
        start_idx = 0

    end_idx = index + hwnd_size + 2
    if end_idx>full_length:
        end_idx = full_length

    count = 0
    for x in range(start_idx, end_idx):
        sumv += out_df.at[x, col_name]
        count += 1

    return sumv/count


def update_eq_avg(old_df, out_df, hwnd_size, col_name):

    out_len = out_df[const.dt_col_name].size
    old_len = old_df[const.dt_col_name].size
    full_wnd_size = (2*hwnd_size+1)
    if old_len < full_wnd_size:
        old_len = 0
    else:
        old_len -= full_wnd_size

    for x in range(0, old_len):
        out_df.at[x, col_name] = old_df.at[x, col_name]

    for x in range(old_len, out_len):
        out_df.at[x, col_name] = calc_avg_value(out_df, x, hwnd_size, out_len)

    # фильтр для сглаживания
    old_len = old_df[const.dt_col_name].size
    filter_hwnd_size = hwnd_size
    count = 3

    if hwnd_size >= 80:
        filter_hwnd_size = round(hwnd_size/6.0)

    for t in range(0, count):
        for x in range(old_len, out_len):
            out_df.at[x, col_name] = smooth_filter(out_df, x, filter_hwnd_size, out_len, col_name)

    return out_df


def update_eq_purify(old_df, out_df, pcol_name, col_name, prev_col_name):

    out_len = out_df[const.dt_col_name].size
    old_len = old_df[const.dt_col_name].size

    for x in range(0, old_len):
        out_df.at[x, pcol_name] = old_df.at[x, pcol_name]

    for x in range(old_len, out_len):
        curr_val = out_df.at[x, col_name]
        prev_val = out_df.at[x, prev_col_name]
        out_df.at[x, pcol_name] = curr_val - prev_val

    return out_df


def update_eq_initial_order(old_df, out_df):

    out_len = out_df[const.dt_col_name].size
    old_len = old_df[const.dt_col_name].size
    mean_value = out_df[const.value_col_name].mean()

    for x in range(old_len, out_len):
        out_df.at[x, const.order_col_name] = mean_value

    return out_df


def update_equations_by_symbol(symbol_str):

    print('Update equations ' + symbol_str + ' ', end='')

    in_file_name = get_cache_filename(symbol_str)
    in_df = pd.read_csv(in_file_name)
    print('..l.', end='')

    out_file_name = get_output_filename(symbol_str)
    if os.path.exists(out_file_name):
        old_df = pd.read_csv(out_file_name)
    else:
        old_df = pd.DataFrame(columns=[const.dt_col_name, const.value_col_name, const.delta1_col_name,
                                       const.delta2_col_name, const.avg7_col_name, const.avg31_col_name,
                                       const.avg181_col_name, const.avg1441_col_name,
                                       const.avg7p_col_name, const.avg31p_col_name, const.avg181p_col_name,
                                       const.order_col_name])
    print('..c.', end='')

    out_df = update_eq_value(in_df, old_df)
    print('..v.', end='')

    out_df = update_eq_delta1(old_df, out_df)
    print('..d1.', end='')

    out_df = update_eq_delta2(old_df, out_df)
    print('..d2.', end='')

    out_df = update_eq_avg(old_df, out_df, const.avg7_hwnd, const.avg7_col_name)
    print('..a7.', end='')

    out_df = update_eq_avg(old_df, out_df, const.avg31_hwnd, const.avg31_col_name)
    print('..a31.', end='')

    out_df = update_eq_avg(old_df, out_df, const.avg181_hwnd, const.avg181_col_name)
    print('..a181.', end='')

    out_df = update_eq_avg(old_df, out_df, const.avg1441_hwnd, const.avg1441_col_name)
    print('..a1441.', end='')

    out_df = update_eq_purify(old_df, out_df, const.avg7p_col_name, const.avg7_col_name, const.avg31_col_name)
    print('..p7.', end='')

    out_df = update_eq_purify(old_df, out_df, const.avg31p_col_name, const.avg31_col_name, const.avg181_col_name)
    print('..p31.', end='')

    out_df = update_eq_purify(old_df, out_df, const.avg181p_col_name, const.avg181_col_name, const.avg1441_col_name)
    print('..p181.', end='')

    out_df = update_eq_initial_order(old_df, out_df)
    print('..ini_ord.', end='')

    out_df.to_csv(out_file_name, index=False, header=True)
    print('..s.', end='')

    print('Completed !')
