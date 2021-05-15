import os
from pconst import const

const.START_UTC = 1620613178

const.TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

const.ADAUSDT = 'ADAUSDT'
const.BCHUSDT = 'BCHUSDT'
const.DOTUSDT = 'DOTUSDT'
const.ETHUSDT = 'ETHUSDT'
const.LINKUSDT = 'LINKUSDT'
const.XTZUSDT = 'XTZUSDT'
const.UNIUSDT = 'UNIUSDT'

# const.BTCUSDT = 'BTCUSDT'
# const.LTCUSDT = 'LTCUSDT'

const.SUFFIX = 'equations'
const.ORDERS = 'orders'

const.avg7_hwnd = 300
const.avg31_hwnd = 500
const.avg181_hwnd = 750
const.avg1441_hwnd = 1000

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
const.avg7p_col_name = 'avg7p'
const.avg31p_col_name = 'avg31p'
const.avg181p_col_name = 'avg181p'
const.order_col_name = 'order'

const.type_col_name = 'type'
const.open_ord_id_col_name = 'open_ord_id'
const.open_dt_col_name = 'open_dt'
const.open_price_col_name = 'open_price'
const.close_ord_id_col_name = 'close_ord_id'
const.close_dt_col_name = 'close_dt'
const.close_price_col_name = 'close_price'
const.qty_col_name = 'qty'
const.qty_in_usd_col_name = 'qty_in_usd'
const.delta_price_col_name = 'delta_price'
const.delta_price_prc_col_name = 'delta_price_prc'
const.profit_col_name = 'profit'
const.profit_prc_col_name = 'profit_prc'
const.sum_profit_col_name = 'sum_profit'
const.sum_profit_prc_col_name = 'sum_profit_prc'

const.order_status_created = 'Created'
const.order_status_rejected = 'Rejected'
const.order_status_new = 'New'
const.order_status_partially_filled = 'PartiallyFilled'
const.order_status_filled = 'Filled'
const.order_status_cancelled = 'Cancelled'
const.order_status_pendingCancel = 'PendingCancel'

const.order_type_limit = 'Limit'
const.order_type_market = 'Market'

const.order_side_buy = 'Buy'
const.order_side_sell = 'Sell'

const.order_time_in_force_good_till_cancel = 'GoodTillCancel'
const.order_time_in_force_immediate_or_cancel = 'ImmediateOrCancel'
const.order_time_in_force_fill_or_kill = 'FillOrKill'
const.order_time_in_force_post_only = 'PostOnly'

const.order_stop_lost_koef_buy = 0.98
const.order_stop_lost_koef_sell = 1.02

const.order_take_profit_koef_buy = 1.02
const.order_take_profit_koef_sell = 0.98

# |d3+d4| must be > (1% of price per 1 hour) = (1/60)*(price/100) = price * (1/6000))
# delta calulates per minute
# 1% per 1 hour = 1/60
# abs(d3 + d4) > price * 0.000167
const.d3_d4_useful_koef = 0.000047
