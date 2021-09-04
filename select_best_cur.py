import os
import json
import requests
import time
import datetime
import pandas as pd
from pconst import const
from consts import *
from client_bybit import *
from update_orders import *
from pprint import pprint
from IPython.core.display import display


def calculate_delta_in_percents(eq_df):

    min = 1000000.0
    max = 0.0
    value_series = eq_df[const.value_col_name]
    df_len = eq_df[const.value_col_name].size
    start = 1  # df_len - const.select_best_wnd_size

    for i in range(start, df_len):
        value = value_series[i]
        if min > value:
            min = value
        if max < value:
            max = value

    result = 100.0 * (max - min) / value
    return result


def calculate_MSE(eq_df):

    value_series = eq_df[const.value_col_name]
    avg96_series = eq_df[const.avg7_col_name]
    df_len = eq_df[const.value_col_name].size
    start = 1  # df_len - const.select_best_wnd_size

    sum = 0.0
    maxe = 0.0
    count = 0
    for i in range(start, df_len):
        delta = abs(value_series[i] - avg96_series[i])
        if delta > maxe:
            maxe = delta
        sum += delta
        count += 1

    # result = sum / (count * value_series[df_len-1])
    result = 100.0 * maxe / value_series[df_len-1]
    return result


# def curr_item_compare(x, y):
#     return x.rmse > y.rmse


def select_best_currencies():
    print('Select most useful currencies...')

    print('    calculate metrics...')
    all_items = []
    for symbol in const.CURRENCIES:
        eq_file_name = get_equations_filename(symbol)
        eq_df = pd.read_csv(eq_file_name)
        curr_delta_p = calculate_delta_in_percents(eq_df)
        curr_mse = calculate_MSE(eq_df)
        curr_dic = {
            'symbol': symbol,
            'delta_p': curr_delta_p,
            'mse': curr_mse,
            'target_func': (curr_delta_p / curr_mse)
        }
        all_items.append(curr_dic)
        print(curr_dic)

    print('    exclude not fitted items...')
    currency_items = []
    for curr_item in all_items:
        if curr_item['delta_p'] > const.select_best_min_delta_prc and curr_item['mse'] < const.select_best_max_mse_prc:
            currency_items.append(curr_item)

    print('    sort metrics...')
    currency_items.sort(key=lambda x: x['target_func'], reverse=True)

    print('    get result...')
    result_list = currency_items[:const.select_best_count]

    for item in currency_items:
        print(item)
    print()

    result = list(map(lambda x: x['symbol'], result_list))
    print(result)
    return result




