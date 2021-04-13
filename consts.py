import os
from pconst import const

const.PUBLIC_API_URL = 'https://api.bybit.com/public/linear/'

const.SERVER_ACCESS_NAME = os.getenv('BYBIT_NAME')
const.SERVER_ACCESS_API_KEY = os.getenv('BYBIT_API_KEY')
const.SERVER_ACCESS_SECRET_CODE = os.getenv('BYBIT_SECRET_CODE')

const.START_UTC = 1617235200

const.BTCUSDT = 'BTCUSDT'
const.BCHUSDT = 'BCHUSDT'
const.ETHUSDT = 'ETHUSDT'
const.LTCUSDT = 'LTCUSDT'
const.LINKUSDT = 'LINKUSDT'
const.XTZUSDT = 'XTZUSDT'
const.ADAUSDT = 'ADAUSDT'
const.DOTUSDT = 'DOTUSDT'
const.UNIUSDT = 'UNIUSDT'

const.SUFFIX = 'equations'
const.ORDERS = 'orders'

const.avg7_hwnd = 3
const.avg31_hwnd = 15
const.avg181_hwnd = 90
const.avg1441_hwnd = 720

const.open_col_name = 'open'
const.close_col_name = 'close'

const.dt_col_name = 'dt'
const.value_col_name = 'value'
const.delta1_col_name = 'delta1'
const.delta2_col_name = 'delta2'
const.avg7_col_name = 'avg7'
const.avg31_col_name = 'avg31'
const.avg181_col_name = 'avg181'
const.avg1441_col_name = 'avg1441'
const.order_col_name = 'order'

const.type_col_name = 'type'
const.open_dt_col_name = 'open_dt'
const.open_price_col_name = 'open_price'
const.close_dt_col_name = 'close_dt'
const.close_price_col_name = 'close_price'
const.delta_price = 'delta_price'
const.delta_price_prc = 'delta_price_prc'
const.profit = 'profit'
const.profit_prc = 'profit_prc'
const.sum_profit = 'sum_profit'
const.sum_profit_prc = 'sum_profit_prc'

const.order_action_open = 'OPEN'
const.order_action_close = 'CLOSE'

const.order_type_buy = 'BUY'
const.order_type_sell = 'SELL'

