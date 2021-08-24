import time
import datetime

from consts import *

const.DEBUG_LOG_FILENAME = 'debug.log'


def debug_log_get_full(symbol_str):
    return r'data/' + const.DEBUG_LOG_FILENAME


def debug_log_write(str):

    curr_dt_utc = datetime.datetime.now()
    curr_ts = curr_dt_utc.timestamp()
    str_dt = datetime.datetime.fromtimestamp(curr_ts).strftime(const.TIME_FORMAT)

    str_val = str_dt + ' : ' + str + '\n'

    f = open(r'data/order.log', 'a')
    f.write(str_val)
    f.close()

    print()
    print(str_val)

