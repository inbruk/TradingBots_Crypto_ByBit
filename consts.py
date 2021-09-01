import os
from pconst import const

const.START_UTC = 1629246728

const.TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

const.BTCUSDT    = 'BTCUSDT'
const.AAVEUSDT   = 'AAVEUSDT'
const.ADAUSDT    = 'ADAUSDT'
const.BCHUSDT    = 'BCHUSDT'
const.DOGEUSDT   = 'DOGEUSDT'
const.DOTUSDT    = 'DOTUSDT'
const.ETHUSDT    = 'ETHUSDT'
const.LINKUSDT   = 'LINKUSDT'
const.LTCUSDT    = 'LTCUSDT'
const.SUSHIUSDT  = 'SUSHIUSDT'
const.XRPUSDT    = 'XRPUSDT'
const.XEMUSDT    = 'XEMUSDT'
const.XTZUSDT    = 'XTZUSDT'
const.UNIUSDT    = 'UNIUSDT'

const.CURRENCIES = [
    const.BTCUSDT,
    const.AAVEUSDT,
    const.ADAUSDT,
    const.BCHUSDT,
    const.DOGEUSDT,
    const.DOTUSDT,
    const.ETHUSDT,
    const.LINKUSDT,
    const.LTCUSDT,
    const.SUSHIUSDT,
    const.XRPUSDT,
    const.XEMUSDT,
    const.XTZUSDT,
    const.UNIUSDT
]

const.SUFFIX = 'equations'
const.ORDERS = 'orders'

const.avg8_wnd = 15
const.avg16_wnd = 15
const.avg24_wnd = 15
const.avg32_wnd = 15
const.avg48_wnd = 15
const.avg64_wnd = 15
const.avg96_wnd = 15
const.avg128_wnd = 15

const.avg_slow_wnd = 15

# best 128, 300
# 1200

const.check_extremum_wnd = 32

const.open_col_name = 'open'
const.close_col_name = 'close'

const.dt_col_name = 'dt'
const.value_col_name = 'value'
const.delta1_col_name = 'delta1'
const.delta2_col_name = 'delta2'
const.avg8_col_name = 'avg8'
const.avg16_col_name = 'avg16'
const.avg24_col_name = 'avg24'
const.avg32_col_name = 'avg32'
const.avg48_col_name = 'avg48'
const.avg64_col_name = 'avg64'
const.avg96_col_name = 'avg96'
const.avg128_col_name = 'avg128'
const.avg_fast_col_name = 'avg_fast'
const.avg_slow_col_name = 'avg_slow'
const.order_col_name = 'order'

const.type_col_name = 'type'
const.open_ord_id_col_name = 'open_ord_id'
const.open_dt_col_name = 'open_dt'
const.open_price_col_name = 'open_price'
const.extremum_col_name = 'extremum'
const.close_ord_id_col_name = 'close_ord_id'
const.close_dt_col_name = 'close_dt'
const.close_price_col_name = 'close_price'
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

const.max_avg_err_wnd_size = 4
const.max_avg_error = 0.02
const.transit_max_pos = 11
const.transit_step = 0.1

const.select_best_wnd_size = 60
const.select_best_min_delta_prc = 8
const.select_best_max_mse_prc = 2.0  # 0.8
const.select_best_count = 4

const.one_curr_order_amount = 45.0

const.order_stop_lost_koef_buy = 0.975
const.order_stop_lost_koef_sell = 1.025

const.order_take_profit_koef_buy = 1.1
const.order_take_profit_koef_sell = 0.9

const.order_create_plus_koef_buy = 1.001
const.order_create_plus_koef_sell = 0.999

# |d3+d4| must be > (1% of price per 1 hour) = (1/60)*(price/100) = price * (1/6000))
# delta calulates per minute
# 1% per 1 hour = 1/60
# abs(d3 + d4) > price * 0.000167
# 0.0003
# 0.000075
# 0.00005
const.min_fast_avg_delta = 0.0000
const.min_slow_avg_delta = 0.0000

const.max_backward_prc = 0.25
