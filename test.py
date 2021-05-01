# import os
# import json
# import requests
# import hashlib
# import hmac
# import time
# import datetime
# import pandas as pd
# from pconst import const
# from IPython.core.display import display
#
# from consts import *
from client_bybit import *

exists1 = client_position_check(const.order_side_buy, const.XTZUSDT)
exists2 = client_position_check(const.order_side_sell, const.XTZUSDT)

success1, order_id, time_now, qty, qty_in_usd, price = client_position_open(const.order_side_buy, const.XTZUSDT, 4, 5.689)
exists3 = client_position_check(const.order_side_buy, const.XTZUSDT)
exists4 = client_position_check(const.order_side_sell, const.XTZUSDT)
success1, order_id, time_now, qty, qty_in_usd, price = client_position_close(const.order_side_buy, const.XTZUSDT, 4, 5.689)

exists5 = client_position_check(const.order_side_buy, const.XTZUSDT)
exists6 = client_position_check(const.order_side_sell, const.XTZUSDT)

time.sleep(5)

success3, order_id, time_now, qty, qty_in_usd, price = client_position_open(const.order_side_sell, const.XTZUSDT, 3, 5.689)
exists7 = client_position_check(const.order_side_buy, const.XTZUSDT)
exists8 = client_position_check(const.order_side_sell, const.XTZUSDT)
success4, order_id, time_now, qty, qty_in_usd, price = client_position_close(const.order_side_sell, const.XTZUSDT, 3, 5.689)

exists9 = client_position_check(const.order_side_buy, const.XTZUSDT)
exists10 = client_position_check(const.order_side_sell, const.XTZUSDT)
sum=0.0
