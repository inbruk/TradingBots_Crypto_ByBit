import os
import json
import requests
import time
import datetime
import pandas as pd
from pconst import const
from IPython.core.display import display

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

const.order_col_name = 'order'

const.open_col_name = 'open'
const.close_col_name = 'close'


def get_cache_filename(symbol_str):
    return r'data/' + symbol_str.lower() + '.csv'


def get_output_filename(symbol_str):
    return r'data/' + symbol_str.lower() + '_' + const.SUFFIX + '.csv'


def update_eq_value(in_df, old_df):

    out_df = pd.DataFrame(columns=[const.dt_col_name, const.value_col_name, const.delta1_col_name,
                                   const.delta2_col_name, const.avg7_col_name, const.avg31_col_name,
                                   const.avg181_col_name, const.avg1441_col_name,
                                   const.avg7l_col_name, const.avg31l_col_name,
                                   const.avg181l_col_name, const.avg1441l_col_name,
                                   const.order_col_name])

    for index, item in in_df.iterrows():
        new_row = {
            const.dt_col_name: item[const.dt_col_name],
            const.value_col_name: 0.0,
            const.delta1_col_name: 0.0,
            const.delta2_col_name: 0.0,
            const.avg7_col_name: 0.0,
            const.avg31_col_name: 0.0,
            const.avg181_col_name: 0.0,
            const.avg1441_col_name: 0.0,
            const.avg7l_col_name: 0.0,
            const.avg31l_col_name: 0.0,
            const.avg181l_col_name: 0.0,
            const.avg1441l_col_name: 0.0,
            const.order_col_name: 0.0
        }
        out_df = out_df.append(new_row, ignore_index=True)

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

    end_idx = index + hwnd_size + 2
    if end_idx>full_length:
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
        old_len -= hwnd_size

    for x in range(0, old_len):
        out_df.at[x, col_name] = old_df.at[x, col_name]

    for x in range(old_len, out_len):
        out_df.at[x, col_name] = calc_avg_value(out_df, x, hwnd_size, out_len)

    # фильтр для сглаживания
    filter_hwnd_size = round(hwnd_size/6.0)
    for x in range(old_len, out_len):
        out_df.at[x, col_name] = smooth_filter(out_df, x, filter_hwnd_size, out_len, col_name)

    return out_df


def update_eq_purify(old_df, out_df, hwnd_size, col_name, prev_col_name):

    out_len = out_df[const.dt_col_name].size
    old_len = old_df[const.dt_col_name].size
    full_wnd_size = (2*hwnd_size+1)
    if old_len < full_wnd_size:
        old_len = 0
    else:
        old_len -= hwnd_size

    for x in range(old_len, out_len):
        out_df.at[x, col_name] = out_df.at[x, col_name] - out_df.at[x, prev_col_name]

    return out_df


def update_eq_linearize(out_df, col_name, new_col_name):

    out_len = out_df[const.dt_col_name].size
    start_x = 0
    start_v = out_df.at[start_x, col_name]
    end_x = 1
    end_v = out_df.at[end_x, col_name]
    if end_v >= start_v:
        it_rised = True
    else:
        it_rised = False

    out_df.at[0, new_col_name] = start_v
    out_df.at[1, new_col_name] = end_v

    for curr_x in range(2, out_len):

        curr_v = out_df.at[curr_x, col_name]

        if curr_v >= end_v:
            new_rised = True
        else:
            new_rised = False

        if (it_rised != new_rised) | (curr_x >= out_len-1):   # draw line

            delta = (curr_v-start_v)/(curr_x - start_x)
            for xx in range(start_x, end_x):
                ix = xx - start_x
                curr_val = start_v + ix * delta
                out_df.at[xx, new_col_name] = curr_val

            it_rised = new_rised
            start_x = end_x
            start_v = end_v

        end_x = curr_x
        end_v = out_df.at[end_x, col_name]

    return out_df


def check_order_start(out_df, x, o_now, o_buy):

    delta1441 = out_df.at[x, const.avg1441l_col_name] - out_df.at[x-1, const.avg1441l_col_name]
    delta181 = out_df.at[x, const.avg181l_col_name] - out_df.at[x-1, const.avg181l_col_name]
    delta31 = out_df.at[x, const.avg31l_col_name] - out_df.at[x-1, const.avg31l_col_name]
    delta7 = out_df.at[x, const.avg7l_col_name] - out_df.at[x-1, const.avg7l_col_name]
    dt = out_df.at[x, const.dt_col_name]
    price = out_df.at[x, const.value_col_name]

    if not o_now:
        if delta1441 > 0 and delta181 > 0 and delta31 > 0 and delta7 > 0:
            o_now = True
            o_buy = True
            print('Open buy order at ', dt, ', price ', price)

        if delta1441 < 0 and delta181 < 0 and delta31 < 0 and delta7 < 0:
            o_now = True
            o_buy = False
            print('Open sell order at ', dt, ', price ', price)
    else:
        if o_buy:
            if (delta1441 + delta181) < 0:
                o_now = False
                print('Close buy order at ', dt, ', price ', price)
        else:
            if (delta1441 + delta181) > 0:
                o_now = False
                print('Close sell order at ', dt, ', price ', price)

    return o_now, o_buy


def fill_order_values(out_df, x, o_now, o_buy, mean_value, min_value, max_value):

    if o_now:
        if o_buy:
            out_df.at[x, const.order_col_name] = max_value
        else:
            out_df.at[x, const.order_col_name] = min_value
    else:
        out_df.at[x, const.order_col_name] = mean_value

    return out_df


def update_eq_order(out_df):

    order_now = False
    order_buy = True

    mean_value = out_df[const.value_col_name].mean()
    min_value = out_df[const.value_col_name].min()
    max_value = out_df[const.value_col_name].max()

    out_len = out_df[const.dt_col_name].size

    out_df.at[0, const.order_col_name] = mean_value
    out_df.at[1, const.order_col_name] = mean_value

    for x in range(2, out_len):
        order_now, order_buy = check_order_start(out_df, x, order_now, order_buy)
        out_df = fill_order_values(out_df, x, order_now, order_buy, mean_value, min_value, max_value)

    return out_df


def update_equations(symbol_str):

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
                                       const.avg7l_col_name, const.avg31l_col_name,
                                       const.avg181l_col_name, const.avg1441l_col_name,
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

    out_df = update_eq_purify(old_df, out_df, const.avg7_hwnd, const.avg7_col_name, const.avg31_col_name)
    print('..p7.', end='')

    out_df = update_eq_purify(old_df, out_df, const.avg31_hwnd, const.avg31_col_name, const.avg181_col_name)
    print('..p31.', end='')

    out_df = update_eq_purify(old_df, out_df, const.avg181_hwnd, const.avg181_col_name, const.avg1441_col_name)
    print('..p181.', end='')

    out_df = update_eq_linearize(out_df, const.avg7_col_name, const.avg7l_col_name)
    print('..l7.', end='')

    out_df = update_eq_linearize(out_df, const.avg31_col_name, const.avg31l_col_name)
    print('..l31.', end='')

    out_df = update_eq_linearize(out_df, const.avg181_col_name, const.avg181l_col_name)
    print('..l181.', end='')

    out_df = update_eq_linearize(out_df, const.avg1441_col_name, const.avg1441l_col_name)
    print('..l1441.')

    out_df = update_eq_order(out_df)
    print('..order.', end='')

    out_df.to_csv(out_file_name, index=False, header=True)
    print('..s!')


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
