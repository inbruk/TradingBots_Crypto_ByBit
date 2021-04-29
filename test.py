import os
import json
import requests
import hashlib
import hmac
import time
import datetime
import pandas as pd
from pconst import const
from IPython.core.display import display

from consts import *
from client_bybit import *


success, order_id, time_now, price, qty_in_usd = client_order_create(const.order_side_buy, const.XTZUSDT, 0.39, 5.242)
success, order_status = client_order_get_status(order_id, const.XTZUSDT)
success, side, size, position_value, entry_price = client_position_read(const.XTZUSDT)

success, order_id, time_now, price, qty_in_usd = client_order_create(const.order_side_sell, const.XTZUSDT, 0.39, 5.242)
success, order_status = client_order_get_status(order_id, const.XTZUSDT)
success, side, size, position_value, entry_price = client_position_read(const.XTZUSDT)


