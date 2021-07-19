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
from IPython.core.display import display


def calculate_delta_in_percents(eq_df):

    min = 1000000.0
    max = 0.0
    value_series = eq_df[const.value_col_name]
    df_len = eq_df[const.value_col_name].size
    start = df_len - const.select_best_wnd_size

    for i in range(start, df_len):
        value = value_series[i]
        if min > value:
            min = value
        if max < value:
            max = value

    result = (max - min)/value
    return result


def calculate_RMSE(eq_df):

    value_series = eq_df[const.value_col_name]
    avg96_series = eq_df[const.avg96_col_name]
    df_len = eq_df[const.value_col_name].size
    start = df_len - const.select_best_wnd_size

    sum = 0.0
    count = 0
    for i in range(start, df_len):
        delta_square = pow((value_series - avg96_series), 2)
        sum += delta_square
        count += 1

    result = sum / count
    return result


def curr_item_compare(x, y):
    return x.rmse > y.rmse


def select_best_currencies(count):
    print('Select most useful currencies...')

    print('    calculate metrics...')
    currency_items = []
    for symbol in const.CURRENCIES:
        eq_file_name = get_equations_filename(symbol)
        eq_df = pd.read_csv(eq_file_name)
        curr_delta_p = calculate_delta_in_percents(eq_df)
        if curr_delta_p > const.select_best_min_delta:
            curr_rmse = calculate_RMSE(eq_df)
            curr_dic = {
                'symbol': symbol,
                'delta_p': curr_delta_p,
                'rmse': curr_rmse
            }
            currency_items.append(curr_dic)
            print(curr_dic)

    print('    sort metrics...')
    sorted(currency_items, cmp=curr_item_compare)

    print(currency_items)

    result = currency_items[:const.select_best_count].symbol
    print(result)
    return result




