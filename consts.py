import os
from pconst import const

const.PUBLIC_API_URL = 'https://api.bybit.com/linear/public/'

const.SERVER_ACCESS_NAME = os.getenv('BYBIT_NAME')
const.SERVER_ACCESS_API_KEY = os.getenv('BYBIT_API_KEY')
const.SERVER_ACCESS_SECRET_CODE = os.getenv('BYBIT_SECRET_CODE')

const.START_UTC = 1609515482

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


