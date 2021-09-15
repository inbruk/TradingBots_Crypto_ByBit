import os
import json
import requests
import time
import datetime
import pandas as pd
from pconst import const
from consts import *
from debug_log import *
from IPython.core.display import display


def get_cache_filename(symbol_str):
    return r'data/' + symbol_str.lower() + '.csv'


def get_output_filename(symbol_str):
    return r'data/' + symbol_str.lower() + '_' + const.SUFFIX + '.csv'


def update_eq_value(in_df, old_df):
    num_rows = in_df[const.dt_col_name].size
    out_df = pd.DataFrame(index=range(num_rows),
                          columns=[const.dt_col_name, const.value_col_name, const.delta1_col_name,
                                   const.delta2_col_name, const.avg2_col_name, const.avg3_col_name,
                                   const.avg4_col_name, const.avg5_col_name, const.avg6_col_name,
                                   const.avg7_col_name, const.avg8_col_name, const.avg_slow_col_name,
                                   const.avg_fast_col_name, const.order_col_name])

    for index, item in in_df.iterrows():
        dt = round(item[const.dt_col_name])
        out_df.at[index,const.dt_col_name] = dt
        out_df.at[index,const.value_col_name] = 0.0,
        out_df.at[index,const.delta1_col_name] = 0.0,
        out_df.at[index,const.delta2_col_name] = 0.0,
        out_df.at[index,const.avg2_col_name] = 0.0,
        out_df.at[index,const.avg3_col_name] = 0.0,
        out_df.at[index,const.avg4_col_name] = 0.0,
        out_df.at[index,const.avg5_col_name] = 0.0,
        out_df.at[index,const.avg6_col_name] = 0.0,
        out_df.at[index,const.avg7_col_name] = 0.0,
        out_df.at[index,const.avg8_col_name] = 0.0,
        out_df.at[index,const.avg_slow_col_name] = 0.0,
        out_df.at[index,const.avg_fast_col_name] = 0.0,
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


def calc_avg_value(out_df, index, hwnd_size, full_length, src_col_name):

    start_idx = index - hwnd_size
    if start_idx < 0:
        start_idx = 0

    end_idx = index + 1  # important place !!! error in wnd size broke all calcs !
    if end_idx > full_length:
        end_idx = full_length

    sumv = 0.0
    divider = 0
    for x in range(start_idx, end_idx):
        value = out_df.at[x, src_col_name]
        sumv += value
        divider += 1

    return sumv/divider


def calc_avg_value2(out_df, index, hwnd_size, full_length, src_col_name):

    start_idx = index - hwnd_size
    if start_idx < 0:
        start_idx = 0

    end_idx = index + 1  # important place !!! error in wnd size broke all calcs !
    if end_idx > full_length:
        end_idx = full_length

    sumv = 0.0
    divider = 0
    curr_add = 1
    # debug_values = ''
    # count = 0
    for x in range(start_idx, end_idx):
        divider += curr_add
        # try:
        value = out_df.at[x, src_col_name] * curr_add
        # except:
        #     value = 0.0
        sumv += value
        curr_add += 1

        # debug_values = debug_values + str(value) + ', '
        # count += 1

    # -------------------------------------------------------------------------------------
    # if hwnd_size == const.avg_slow_wnd:
    #     debug_log_write('calc_avg_value:')
    #     curr_dt = out_df.at[start_idx, const.dt_col_name]
    #     debug_log_write('    dt=' + str(curr_dt) + ' start_idx=' + str(start_idx) + ' end_idx=' + str(end_idx) + ' count=' + str(count))
    #     debug_log_write('    hwnd_size=' + str(hwnd_size) + ' start_idx=' + str(start_idx) + ' end_idx=' + str(end_idx))
    #     debug_log_write('    debug_values' + debug_values)
    # -------------------------------------------------------------------------------------

    return sumv/divider


def calc_avg_value3(out_df, index, hwnd_size, full_length, src_col_name):

    start_idx = index - hwnd_size
    if start_idx < 0:
        start_idx = 0

    end_idx = index + 1  # important place !!! error in wnd size broke all calcs !
    if end_idx > full_length:
        end_idx = full_length

    sumv = 0.0
    divider = 1
    for x in range(start_idx, end_idx):
        curr_add = end_idx - x
        value = out_df.at[x, src_col_name] * curr_add
        sumv += value
        divider += curr_add

    return sumv/divider


def smooth_filter(out_df, index, hwnd_size, full_length, col_name):
    sumv = 0.0

    start_idx = index - hwnd_size
    if start_idx < 0:
        start_idx = 0

    end_idx = index + 1  # + hwnd_size + 1   # warpath calculation
    if end_idx > full_length:
        end_idx = full_length

    count = 0
    for x in range(start_idx, end_idx):
        sumv += out_df.at[x, col_name]
        count += 1

    return sumv/count


def update_eq_avg(old_df, out_df, src_col_name, hwnd_size, dst_col_name):

    out_len = out_df[const.dt_col_name].size
    old_len = old_df[const.dt_col_name].size
    full_wnd_size = (2*hwnd_size+1)
    if old_len < full_wnd_size:
        old_len = 0
    else:
        old_len -= full_wnd_size

    for x in range(0, old_len):
        out_df.at[x, dst_col_name] = old_df.at[x, dst_col_name]

    for x in range(old_len, out_len):
        out_df.at[x, dst_col_name] = calc_avg_value(out_df, x, hwnd_size, out_len, src_col_name)

    return out_df


def combine_2_values(out_df, x, src_col1_name, src_col2_name, koef):
    da1 = abs(out_df.at[x, src_col1_name] - out_df.at[x-1, src_col1_name])
    da2 = abs(out_df.at[x, src_col2_name] - out_df.at[x-1, src_col2_name])

    result = out_df.at[x, src_col1_name]
    if da1 > koef*da2:
        result = out_df.at[x, src_col2_name]

    return result


def combine_eq_avg(old_df, out_df, src_col1_name, src_col2_name, koef, dst_col_name):

    out_len = out_df[const.dt_col_name].size
    old_len = old_df[const.dt_col_name].size

    out_df.at[0, dst_col_name] = out_df.at[0, src_col1_name]

    for x in range(1, old_len):
        out_df.at[x, dst_col_name] = old_df.at[x, dst_col_name]

    if old_len < 1:
        old_len = 1

    for x in range(old_len, out_len):
        out_df.at[x, dst_col_name] = combine_2_values(out_df, x, src_col1_name, src_col2_name, koef)

    return out_df


def filter_p1(val, val_prev, koef):

    if koef < 0:
        raise ValueError('In filter_p1() parameter koef must be > 0 !!!')

    delta = (val - val_prev) / val_prev
    dabs = abs(delta)

    sign = 1.0
    if delta < 0.0:
        sign = -1.0

    if dabs > koef:
        delta = sign * koef
        res = val_prev + delta * val

    return res


def filter_p1_eq_avg(old_df, out_df, src_col_name, koef, dst_col_name):

    out_len = out_df[const.dt_col_name].size
    old_len = old_df[const.dt_col_name].size

    out_df.at[0, dst_col_name] = out_df.at[0, src_col_name]

    for x in range(1, old_len):
        out_df.at[x, dst_col_name] = old_df.at[x, dst_col_name]

    if old_len < 1:
        old_len = 1

    for x in range(old_len, out_len):
        val = out_df.at[x, src_col_name]
        val_prev = out_df.at[x-1, dst_col_name]
        val = filter_p1(val, val_prev, koef)
        out_df.at[x, dst_col_name] = val

    return out_df


def filter_p2(val, val_prev, val_pp, koef):

    if koef < 0:
        raise ValueError('In filter_p2() parameter koef must be > 0 !!!')

    d1_1 = (val - val_prev) / val_prev
    d1_2 = (val_prev - val_pp) / val_prev
    d2 = d1_1 - d1_2

    d2abs = abs(d2)

    sign = 1.0
    if d2abs < 0.0:
        sign = -1.0

    if d2abs > koef:
        d2 = sign * koef
        d1_1 = d1_2 + d2
        val = val_prev + d1_1 * val_prev

    return val


def filter_p2_eq_avg(old_df, out_df, src_col_name, koef, dst_col_name):

    out_len = out_df[const.dt_col_name].size
    old_len = old_df[const.dt_col_name].size

    out_df.at[0, dst_col_name] = out_df.at[0, src_col_name]
    out_df.at[1, dst_col_name] = out_df.at[1, src_col_name]

    for x in range(2, old_len):
        out_df.at[x, dst_col_name] = old_df.at[x, dst_col_name]

    if old_len < 2:
        old_len = 2

    for x in range(old_len, out_len):
        val = out_df.at[x, src_col_name]
        val_prev = out_df.at[x-1, dst_col_name]
        val_pp = out_df.at[x-2, dst_col_name]
        val = filter_p2(val, val_prev, val_pp, koef)
        out_df.at[x, dst_col_name] = val

    return out_df


count_use_avg128 = 0
count_use_avg96 = 0
count_use_avg64 = 0
count_use_avg48 = 0
count_use_avg32 = 0
count_use_avg24 = 0
count_use_avg16 = 0
count_use_avg8 = 0

prev_col = const.avg8_col_name
next_col = const.avg8_col_name
is_transit_now = False
curr_transit_pos = 1


def calc_avg_cols_usage(curr_col):
    global count_use_avg128
    global count_use_avg96
    global count_use_avg64
    global count_use_avg48
    global count_use_avg32
    global count_use_avg24
    global count_use_avg16
    global count_use_avg8

    if curr_col == const.avg8_col_name:
        count_use_avg128 += 1
    else:
        if curr_col == const.avg7_col_name:
            count_use_avg96 += 1
        else:
            if curr_col == const.avg6_col_name:
                count_use_avg64 += 1
            else:
                if curr_col == const.avg5_col_name:
                    count_use_avg48 += 1
                else:
                    if curr_col == const.avg4_col_name:
                        count_use_avg32 += 1
                    else:
                        if curr_col == const.avg3_col_name:
                            count_use_avg24 += 1
                        else:
                            if curr_col == const.avg2_col_name:
                                count_use_avg16 += 1
                            else:
                                if curr_col == const.avg1_col_name:
                                    count_use_avg8 += 1


def get_avg_col_error(out_df, x, curr_col):
    col_value = out_df.at[x, curr_col]
    value = out_df.at[x, const.value_col_name]
    return abs(value - col_value)/value


def is_avg_col_error_more_const(out_df, x, curr_col, error):

    if x < const.max_avg_err_wnd_size+1:
        return False

    start = x - const.max_avg_err_wnd_size

    sum = 0.0
    cnt = 0
    for i in range(start, x+1):
        sum += get_avg_col_error(out_df, i, curr_col)
        cnt += 1

    return (sum/cnt) > error


def calc_curr_col(out_df, x):

    if is_transit_now:
        return next_col
    else:
        curr_col = const.avg8_col_name
        # if is_avg_col_error_more_const(out_df, x, curr_col, const.max_avg_error):
            # curr_col = const.avg64_col_name
            # if is_avg_col_error_more_const(out_df, x, curr_col, const.max_avg_error):
            #     curr_col = const.avg48_col_name
            #     if is_avg_col_error_more_const(out_df, x, curr_col, const.max_avg_error):
            #         curr_col = const.avg32_col_name
            #         if is_avg_col_error_more_const(out_df, x, curr_col, const.max_avg_error):
            # curr_col = const.avg24_col_name
            # if is_avg_col_error_more_const(out_df, x, curr_col, const.max_avg_error):
            # curr_col = const.avg16_col_name
            # if is_avg_col_error_more_const(out_df, x, curr_col, const.max_avg_error):
            #     curr_col = const.avg8_col_name

    return curr_col


def linear_approx_2values(out_df, x):

    global curr_transit_pos
    global is_transit_now
    global prev_col
    global next_col

    prev_value = out_df.at[x, prev_col]
    next_value = out_df.at[x, next_col]
    k = curr_transit_pos*const.transit_step
    result = prev_value * (1 - k) + next_value * k

    if curr_transit_pos > const.transit_max_pos/2.0:
        calc_avg_cols_usage(next_col)
    else:
        calc_avg_cols_usage(prev_col)

    curr_transit_pos += 1
    if curr_transit_pos >= const.transit_max_pos:
        prev_col = next_col
        curr_transit_pos = 1
        is_transit_now = False

    return result


def get_avg_fast_value(out_df, x):

    global count_use_avg128
    global count_use_avg96
    global count_use_avg64
    global count_use_avg48
    global count_use_avg32
    global count_use_avg24
    global count_use_avg16
    global count_use_avg8

    global curr_transit_pos
    global is_transit_now
    global prev_col
    global next_col

    if is_transit_now:
        result = linear_approx_2values(out_df, x)
    else:
        curr_col = calc_curr_col(out_df, x)

        if prev_col != curr_col:
            next_col = curr_col
            is_transit_now = True
            curr_transit_pos = 1

            result = linear_approx_2values(out_df, x)
        else:
            result = out_df.at[x, prev_col]
            calc_avg_cols_usage(prev_col)

    return result


def avg_fast_percents_str():

    sum = count_use_avg128 + count_use_avg96 + count_use_avg64 + \
          count_use_avg48 + count_use_avg32 + count_use_avg24 + count_use_avg16 + count_use_avg8

    percents_use_avg128 = round(100.0*count_use_avg128/sum, 0)
    percents_use_avg96 = round(100.0*count_use_avg96/sum, 0)
    percents_use_avg64 = round(100.0*count_use_avg64/sum, 0)
    percents_use_avg48 = round(100.0*count_use_avg48/sum, 0)
    percents_use_avg32 = round(100.0*count_use_avg32/sum, 0)
    percents_use_avg24 = round(100.0 * count_use_avg24 / sum, 0)
    percents_use_avg16 = round(100.0 * count_use_avg16 / sum, 0)
    percents_use_avg8 = round(100.0 * count_use_avg8 / sum, 0)

    result = '(' + str(percents_use_avg128) + ' ' + str(percents_use_avg96) + ' ' + str(percents_use_avg64) + ' ' + \
             str(percents_use_avg48) + ' ' + str(percents_use_avg32) + ' ' + str(percents_use_avg24) + ' ' + \
             str(percents_use_avg16) + ' ' + str(percents_use_avg8) + ')'

    return result


def update_avg_fast_col(old_df, out_df):

    out_len = out_df[const.dt_col_name].size
    old_len = old_df[const.dt_col_name].size

    for x in range(0, old_len):
        out_df.at[x, const.avg_fast_col_name] = old_df.at[x, const.avg_fast_col_name]

    for x in range(old_len, out_len):
        out_df.at[x, const.avg_fast_col_name] = get_avg_fast_value(out_df, x)

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
                                       const.delta2_col_name, const.avg2_col_name, const.avg3_col_name,
                                       const.avg4_col_name, const.avg5_col_name, const.avg6_col_name,
                                       const.avg7_col_name, const.avg8_col_name, const.avg_slow_col_name,
                                       const.avg_fast_col_name, const.order_col_name])
    print('..c.', end='')

    out_df = update_eq_value(in_df, old_df)
    print('..v.', end='')

    out_df = update_eq_delta1(old_df, out_df)
    print('..d1.', end='')

    out_df = update_eq_delta2(old_df, out_df)
    print('..d2.', end='')

    out_df = update_eq_avg(old_df, out_df, const.value_col_name, const.avg1_wnd, const.avg1_col_name)
    print('..a1.', end='')

    out_df = filter_p2_eq_avg(old_df, out_df, const.avg1_col_name, 0.0001, const.avg2_col_name)
    print('..a2.', end='')

    out_df = update_eq_avg(old_df, out_df, const.value_col_name, const.avg3_wnd, const.avg3_col_name)
    print('..a3.', end='')

    out_df = filter_p2_eq_avg(old_df, out_df, const.avg3_col_name, 0.0001, const.avg4_col_name)
    print('..a4.', end='')

    out_df = update_eq_avg(old_df, out_df, const.value_col_name, const.avg5_wnd, const.avg5_col_name)
    print('..a5.', end='')

    out_df = filter_p2_eq_avg(old_df, out_df, const.avg5_col_name, 0.0001, const.avg6_col_name)
    print('..a6.', end='')

    out_df = update_eq_avg(old_df, out_df, const.value_col_name, const.avg7_wnd, const.avg7_col_name)
    print('..a7.', end='')

    out_df = update_eq_avg(old_df, out_df, const.value_col_name, const.avg8_wnd, const.avg8_col_name)
    print('..a8.', end='')

    out_df = update_eq_avg(old_df, out_df, const.value_col_name, const.avg_slow_wnd, const.avg_slow_col_name)
    print('..avg_slow.', end='')

    out_df = update_avg_fast_col(old_df, out_df)
    percents_str = avg_fast_percents_str()
    print('..avg_fast' + percents_str + '..', end='')

    out_df = update_eq_initial_order(old_df, out_df)
    print('..ini_ord.', end='')

    out_df.to_csv(out_file_name, index=False, header=True)
    print('..s.', end='')

    print('Completed !')
