import os
import json
import requests
import time
import datetime
import pandas as pd
from pconst import const
from consts import *
from client_bybit import *
from debug_log import *
from IPython.core.display import display


def get_equations_filename(symbol_str):
    return r'data/' + symbol_str.lower() + '_' + const.SUFFIX + '.csv'


def get_orders_filename(symbol_str):
    return r'data/' + symbol_str.lower() + '_' + const.ORDERS + '.csv'


def check_for_extremum_in_wnd(out_df, index):
    has_pos = False
    has_neg = False
    out_len = out_df[const.dt_col_name].size

    start_idx = index - const.check_extremum_wnd
    if start_idx < 0:
        start_idx = 0

    end_idx = index
    if end_idx > out_len:
        end_idx = out_len

    for x in range(start_idx, end_idx):
        delta = out_df.at[x+1, const.avg_fast_col_name] - out_df.at[x, const.avg_fast_col_name]
        if delta > 0:
            has_pos = True
        if delta < 0:
            has_neg = True

    return has_pos, has_neg


def check_order_open_close(out_df, x, o_now, o_buy, beg_value, ord_df):

    delta1 = out_df.at[x, const.avg1_col_name] - out_df.at[x - 1, const.avg1_col_name]
    # delta2 = out_df.at[x, const.avg2_col_name] - out_df.at[x - 1, const.avg2_col_name]
    # delta3 = out_df.at[x, const.avg3_col_name] - out_df.at[x - 1, const.avg3_col_name]
    # delta4 = out_df.at[x, const.avg4_col_name] - out_df.at[x - 1, const.avg4_col_name]
    # delta5 = out_df.at[x, const.avg5_col_name] - out_df.at[x - 1, const.avg5_col_name]
    # delta6 = out_df.at[x, const.avg6_col_name] - out_df.at[x - 1, const.avg6_col_name]
    # delta7 = out_df.at[x, const.avg7_col_name] - out_df.at[x - 1, const.avg7_col_name]
    # delta8 = out_df.at[x, const.avg8_col_name] - out_df.at[x - 1, const.avg8_col_name]

    # dt = round(out_df.at[x, const.dt_col_name])
    price = out_df.at[x, const.value_col_name]
    avg_slow_value = out_df.at[x, const.avg_slow_col_name]
    avg_fast_value = out_df.at[x, const.avg_fast_col_name]

    delta_slow = avg_slow_value - out_df.at[x - 1, const.avg_slow_col_name]
    delta_fast = avg_fast_value - out_df.at[x - 1, const.avg_fast_col_name]

    o_change = False

    fast_koef = price * const.min_fast_avg_delta
    slow_koef = price * const.min_slow_avg_delta

    if not o_now:

        if abs(delta_slow) > slow_koef and abs(delta_fast) > fast_koef:
            if delta_fast > 0 and delta_slow > 0:  # and avg_fast_value >= avg_slow_value:  # and price > avg_fast_value
                o_change = True
                o_now = True
                o_buy = True
            if delta_fast < 0 and delta_slow < 0:  # and avg_fast_value <= avg_slow_value:  # and price < avg_fast_value
                o_change = True
                o_now = True
                o_buy = False

    else:

        curr_ord_pos = len(ord_df) - 1
        extremum = ord_df.at[curr_ord_pos, const.extremum_col_name]
        extr_beg = ord_df.at[curr_ord_pos, const.extr_beg_col_name]

        if extremum == 0.0:
            extremum = avg_fast_value
            extr_beg = avg_fast_value
        else:

            if (o_buy and extr_beg > avg_fast_value) or \
               (not o_buy and extr_beg < avg_fast_value) or \
               (o_buy and delta_slow < 0) or \
               (not o_buy and delta_slow > 0):  # or \
               # (o_buy and avg_fast_value < avg_slow_value) or \
               # (not o_buy and avg_fast_value > avg_slow_value):
               # (o_buy and price < avg_fast_value) or \
               # (not o_buy and price > avg_fast_value):
                o_change = True
                o_now = False
                return o_now, o_buy, o_change

            if extremum != extr_beg:
                if o_buy:
                    backward_koef = (extremum - avg_fast_value) / abs(extremum - extr_beg)
                else:
                    backward_koef = (avg_fast_value - extremum) / abs(extr_beg - extremum)

                ref_profit = abs(avg_fast_value - extr_beg) / price

                if backward_koef > const.max_backward_prc:  # or \
                   # (o_buy and delta_fast < 0 and ref_profit > const.chain_fast_ref_profit) or \
                   # (not o_buy and delta_fast > 0 and ref_profit > const.chain_fast_ref_profit):
                    o_change = True
                    o_now = False
                    return o_now, o_buy, o_change

            if o_buy:
                if avg_fast_value > extremum:
                    extremum = avg_fast_value
            else:
                if avg_fast_value < extremum:
                    extremum = avg_fast_value

        ord_df.at[curr_ord_pos, const.extremum_col_name] = extremum
        ord_df.at[curr_ord_pos, const.extr_beg_col_name] = extr_beg

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


def fill_order_values(
        ord_df, o_open, o_buy,
        open_order_id, beg_dt, beg_val,
        close_order_id, end_dt, end_val,
        qty_in_usd
):
    len = ord_df[const.type_col_name].size
    if o_open:
        pos = len  # add new row
    else:
        pos = len - 1  # insert values into last row

    if o_open:
        if o_buy:
            ord_df.at[pos, const.type_col_name] = const.order_side_buy
        else:
            ord_df.at[pos, const.type_col_name] = const.order_side_sell

        ord_df.at[pos, const.open_ord_id_col_name] = open_order_id
        ord_df.at[pos, const.open_dt_col_name] = beg_dt
        ord_df.at[pos, const.open_price_col_name] = beg_val
        ord_df.at[pos, const.extremum_col_name] = 0.0
        ord_df.at[pos, const.extr_beg_col_name] = 0.0
        ord_df.at[pos, const.close_ord_id_col_name] = ' '
        ord_df.at[pos, const.close_dt_col_name] = 0.0
        ord_df.at[pos, const.close_price_col_name] = 0.0
        ord_df.at[pos, const.delta_price_col_name] = 0.0
        ord_df.at[pos, const.delta_price_prc_col_name] = 0.0
        ord_df.at[pos, const.profit_col_name] = 0.0
        ord_df.at[pos, const.profit_prc_col_name] = 0.0
        ord_df.at[pos, const.sum_profit_col_name] = 0.0
        ord_df.at[pos, const.sum_profit_prc_col_name] = 0.0
        ord_df.at[pos, const.qty_in_usd_col_name] = 0.0
    else:
        ord_df.at[pos, const.close_ord_id_col_name] = close_order_id
        ord_df.at[pos, const.close_dt_col_name] = end_dt
        ord_df.at[pos, const.close_price_col_name] = end_val
        ord_df.at[pos, const.qty_in_usd_col_name] = qty_in_usd

        if o_buy:
            d_price = end_val - beg_val
        else:
            d_price = beg_val - end_val

        d_price_prc = (d_price / beg_val) * 100.0
        p_prc = d_price_prc
        p = (p_prc/100.0) * qty_in_usd

        ord_df.at[pos, const.delta_price_col_name] = d_price
        ord_df.at[pos, const.delta_price_prc_col_name] = d_price_prc
        ord_df.at[pos, const.profit_col_name] = p
        ord_df.at[pos, const.profit_prc_col_name] = p_prc

        prev = pos - 1
        if prev >= 0:
            ord_df.at[pos, const.sum_profit_col_name] = ord_df.at[prev, const.sum_profit_col_name] + p
            ord_df.at[pos, const.sum_profit_prc_col_name] = ord_df.at[prev, const.sum_profit_prc_col_name] + p_prc
        else:
            ord_df.at[pos, const.sum_profit_col_name] = p
            ord_df.at[pos, const.sum_profit_prc_col_name] = p_prc

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
    open_order_id = ''
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
        if close_dt == 0.0:  # last order not closed
            order_now = True
            if ord_type == const.order_side_buy:
                order_buy = True
            else:
                order_buy = False
            open_order_id = ord_df.at[pos, const.open_ord_id_col_name]
            beg_dt = ord_df.at[pos, const.open_dt_col_name]
            beg_val = ord_df.at[pos, const.open_price_col_name]
        else:
            order_now = False
            order_buy = False
            open_order_id = ''
            beg_dt = 0.0
            beg_val = 0.0

    return order_now, order_buy, open_order_id, beg_dt, beg_val


def check_and_close_when_autoclosed(out_df, ord_df, symbol, order_buy, open_order_id, beg_dt, beg_val, x):
    if order_buy:
        position_exists = client_position_check(const.order_side_buy, symbol)
    else:
        position_exists = client_position_check(const.order_side_sell, symbol)

    if not position_exists:
        end_dt = out_df.at[x, const.dt_col_name]
        end_val = out_df.at[x, const.value_col_name]

        # -------------------------------------------------------------------------------------
        debug_log_write('autoclose order !!! fill_order_values()')
        # -------------------------------------------------------------------------------------

        ord_df = fill_order_values(
            ord_df, False, order_buy, open_order_id, beg_dt, beg_val,
            'autoclosed', end_dt, end_val, const.one_curr_order_amount
        )
        return True, ord_df

    return False, ord_df


def update_eq_order(out_df, ord_df, symbol, qty_in_usd):
    out_len = out_df[const.dt_col_name].size
    x = out_len - 1

    curr_min_utc, prev5_min_utc = get_curr_prev5_minute_utc()
    last_dt_utc = out_df.at[x, const.dt_col_name]

    last_dt = datetime.datetime.fromtimestamp(last_dt_utc).strftime(const.TIME_FORMAT)
    curr_min_dt = datetime.datetime.fromtimestamp(curr_min_utc).strftime(const.TIME_FORMAT)

    print('..[' + last_dt + ',' + curr_min_dt + '].', end='')

    # -------------------------------------------------------------------------------------
    # debug_log_write('update_eq_order -------------------------------------------------------------------- ')
    # debug_log_write('    x=' + str(x) + ' last_dt_utc=' + str(last_dt_utc) + ' last_dt=' + str(last_dt) + ' curr_min_dt=' + str(curr_min_dt))
    # -------------------------------------------------------------------------------------

    ord_change = False
    order_now, order_buy, open_order_id, beg_dt, beg_val = check_for_order_open(ord_df)
    # -------------------------------------------------------------------------------------
    # debug_log_write('check_for_order_open:')
    # debug_log_write('    order_now=' + str(order_now) + ' order_buy=' +str(order_buy) + ' open_order_id=' + str(open_order_id))
    # debug_log_write('    beg_dt=' + str(beg_dt) + ' beg_val=' + str(beg_val))
    # -------------------------------------------------------------------------------------

    if order_now:
        auto_closed, ord_df = check_and_close_when_autoclosed(
            out_df, ord_df, symbol, order_buy, open_order_id, beg_dt, beg_val, x)
        # -------------------------------------------------------------------------------------
        # debug_log_write('check_and_close_when_autoclosed: auto_closed=' + str(auto_closed))
        # -------------------------------------------------------------------------------------
        if auto_closed:
            return out_df, ord_df

    order_now, order_buy, ord_change = check_order_open_close(out_df, x, order_now, order_buy, beg_val, ord_df)
    # -------------------------------------------------------------------------------------
    # debug_log_write('check_order_open_close:')
    # debug_log_write('    order_now=' + str(order_now) + ' order_buy=' + str(order_buy) + ' ord_change=' + str(ord_change))
    # -------------------------------------------------------------------------------------

    if ord_change:
        if order_now:
            if order_buy:
                order_buy_str = const.order_side_buy
            else:
                order_buy_str = const.order_side_sell

            beg_val = out_df.at[x, const.value_col_name]

            success_open, open_order_id, beg_dt, qty, qty_in_usd, beg_val = \
                client_position_open(order_buy_str, symbol, qty_in_usd, beg_val)

            if success_open:
                # -------------------------------------------------------------------------------------
                debug_log_write('client_position_open:')
                debug_log_write(
                    '    success_open=' + str(success_open) + ' open_order_id=' + str(open_order_id) + ' beg_dt=' + str(
                        beg_dt))
                debug_log_write('    qty=' + str(qty) + ' qty_in_usd=' + str(qty_in_usd) + ' beg_val=' + str(beg_val))
                # -------------------------------------------------------------------------------------

                ord_df = fill_order_values(
                    ord_df, order_now, order_buy, open_order_id, beg_dt, beg_val, ' ', 0.0, 0.0, qty_in_usd
                )
            else:
                # -------------------------------------------------------------------------------------
                debug_log_write('client_position_open: FAILS !!!')
                # -------------------------------------------------------------------------------------
        else:
            if order_buy:
                order_buy_str = const.order_side_buy
            else:
                order_buy_str = const.order_side_sell

            end_val = out_df.at[x, const.value_col_name]

            success_close, close_order_id, end_dt, qty, qty_in_usd, end_val = \
                client_position_close(order_buy_str, symbol, qty_in_usd, end_val)

            if success_close:
                # -------------------------------------------------------------------------------------
                debug_log_write('client_position_close:')
                debug_log_write('    success_open=' + str(success_close) + ' open_order_id=' + str(open_order_id) + ' end_dt=' + str(end_dt))
                debug_log_write('    qty=' + str(qty) + ' qty_in_usd=' + str(qty_in_usd) + ' end_val=' + str(end_val))
                # -------------------------------------------------------------------------------------

                ord_df = fill_order_values(
                    ord_df, order_now, order_buy, open_order_id, beg_dt, beg_val,
                    close_order_id, end_dt, end_val, qty_in_usd
                )
            else:
                # -------------------------------------------------------------------------------------
                debug_log_write('client_position_close: FAILS !!!')
                # -------------------------------------------------------------------------------------

    return out_df, ord_df


def fill_eq_by_order(out_df, ord_df):

    out_len = out_df[const.dt_col_name].size

    mean_value = out_df[const.value_col_name].mean()
    min_value = out_df[const.value_col_name].min()
    max_value = out_df[const.value_col_name].max()
    min_value_2 = (mean_value + min_value)/2
    max_value_2 = (mean_value + max_value)/2

    for x in range(0, out_len):
        out_df.at[x, const.order_col_name] = mean_value
        out_df.at[x, const.order_profit_col_name] = mean_value

    ord_len = ord_df[const.type_col_name].size
    last_x = 0
    for pos in range(0, ord_len):
        if ord_df.at[pos, const.close_dt_col_name] != 0.0:
            side = ord_df.at[pos, const.type_col_name]
            profit = ord_df.at[pos, const.profit_col_name]
            beg_dt = ord_df.at[pos, const.open_dt_col_name]
            #  beg_val = ord_df.at[pos, const.open_price_col_name]
            end_dt = ord_df.at[pos, const.close_dt_col_name]
            #  end_val = ord_df.at[pos, const.close_price_col_name]

            temp_x = last_x
            for x in range(last_x, out_len):
                curr_dt = out_df.at[x, const.dt_col_name]
                if beg_dt <= curr_dt <= end_dt:
                    if side == const.order_side_buy:
                        out_df.at[x, const.order_col_name] = max_value
                    else:
                        out_df.at[x, const.order_col_name] = min_value

                    if profit >= 0.0:
                        out_df.at[x, const.order_profit_col_name] = max_value_2
                    else:
                        out_df.at[x, const.order_profit_col_name] = min_value_2

                    temp_x = x

            last_x = temp_x

    return out_df


def fill_orders_by_historical_data(symbol_str):
    print('Fill historical orders ' + symbol_str + ' ', end='')

    eq_file_name = get_equations_filename(symbol_str)
    eq_df = pd.read_csv(eq_file_name)
    print('..load eq.', end='')

    ord_file_name = get_orders_filename(symbol_str)
    if os.path.exists(ord_file_name):
        ord_df = pd.read_csv(ord_file_name)
    else:
        ord_df = pd.DataFrame(columns=[const.type_col_name,
                                       const.open_ord_id_col_name, const.open_dt_col_name, const.open_price_col_name,
                                       const.extremum_col_name, const.extr_beg_col_name,
                                       const.close_ord_id_col_name, const.close_dt_col_name, const.close_price_col_name,
                                       const.qty_in_usd_col_name,
                                       const.delta_price_col_name, const.delta_price_prc_col_name,
                                       const.profit_col_name, const.profit_prc_col_name,
                                       const.sum_profit_col_name, const.sum_profit_prc_col_name])
    print('..load ord.', end='')

    eq_len = eq_df[const.dt_col_name].size
    mean_value = eq_df[const.value_col_name].mean()
    min_value = eq_df[const.value_col_name].min()
    max_value = eq_df[const.value_col_name].max()

    eq_df.at[0, const.order_col_name] = mean_value
    eq_df.at[1, const.order_col_name] = mean_value
    o_now = False
    o_buy = False
    beg_dt = 0
    end_dt = 0
    beg_v = 0.0
    end_v = 0.0
    extremum = 0.0

    for x in range(2, eq_len):
        o_now, o_buy, o_change = check_order_open_close(eq_df, x, o_now, o_buy, beg_v, ord_df)

        if o_now and o_change:
            beg_dt = eq_df.at[x, const.dt_col_name]
            beg_v = eq_df.at[x, const.value_col_name]

        if o_now and not o_change:
            value = eq_df.at[x, const.value_col_name]
            if o_buy:
                if (beg_v * const.order_stop_lost_koef_buy) > value:
                    o_change = True
            else:
                if (beg_v * const.order_stop_lost_koef_sell) < value:
                    o_change = True

        fill_equation_values(eq_df, x, o_now, o_buy, mean_value, min_value, max_value)

        if o_change:
            if o_now:
                beg_dt = eq_df.at[x, const.dt_col_name]

                if o_buy:
                    beg_v = eq_df.at[x, const.value_col_name] * const.order_create_plus_koef_buy
                else:
                    beg_v = eq_df.at[x, const.value_col_name] * const.order_create_plus_koef_sell

                # -------------------------------------------------------------------------------------
                # ord_df = fill_order_values(
                #     ord_df, o_now, o_buy, 'test open order', beg_dt, beg_v, '', 0.0, 0.0, 0.0)
                # -------------------------------------------------------------------------------------

                ord_df = fill_order_values(
                    ord_df, o_now, o_buy, ' ', beg_dt, beg_v, ' ', 0.0, 0.0, const.one_curr_order_amount)

            else:
                end_dt = eq_df.at[x, const.dt_col_name]

                if o_buy:
                    end_v = eq_df.at[x, const.value_col_name] * const.order_create_plus_koef_buy
                else:
                    end_v = eq_df.at[x, const.value_col_name] * const.order_create_plus_koef_sell

                ord_df = fill_order_values(
                    ord_df, o_now, o_buy, ' ', beg_dt, beg_v, ' ', end_dt, end_v, const.one_curr_order_amount)

    print('..fill historical orders.', end='')

    eq_df = fill_eq_by_order(eq_df, ord_df)
    print('..fill eq with orders.', end='')

    ord_df.to_csv(ord_file_name, index=False, header=True)
    print('..save ord.', end='')

    eq_df.to_csv(eq_file_name, index=False, header=True)
    print('..save eq.', end='')

    print('Completed !')


def update_orders_by_symbol(symbol_str, qty_in_usd):
    print('Update orders ' + symbol_str + ' ', end='')

    eq_file_name = get_equations_filename(symbol_str)
    eq_df = pd.read_csv(eq_file_name)
    print('..load eq.', end='')

    ord_file_name = get_orders_filename(symbol_str)
    if os.path.exists(ord_file_name):
        ord_df = pd.read_csv(ord_file_name)
    else:
        ord_df = pd.DataFrame(columns=[const.type_col_name,
                                       const.open_ord_id_col_name, const.open_dt_col_name, const.open_price_col_name,
                                       const.close_ord_id_col_name, const.close_dt_col_name, const.close_price_col_name,
                                       const.extremum_col_name, const.extr_beg_col_name,
                                       const.qty_in_usd_col_name,
                                       const.delta_price_col_name, const.delta_price_prc_col_name,
                                       const.profit_col_name, const.profit_prc_col_name,
                                       const.sum_profit_col_name, const.sum_profit_prc_col_name])
    print('..load ord.', end='')

    eq_df, ord_df = update_eq_order(eq_df, ord_df, symbol_str, qty_in_usd)
    print('..update ord.', end='')

#    eq_df = fill_eq_by_order(eq_df, ord_df)
#    print('..fill eq with orders.', end='')

    ord_df.to_csv(ord_file_name, index=False, header=True)
    print('..save ord.', end='')

    eq_df.to_csv(eq_file_name, index=False, header=True)
    print('..save eq.', end='')

    print('Completed !')
