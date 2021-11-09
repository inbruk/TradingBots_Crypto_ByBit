import os
from pconst import const

const.START_UTC = 1636244620  # 1635120000

const.TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

const.AAVEUSDT   = 'AAVEUSDT'
const.ADAUSDT    = 'ADAUSDT'
const.AVAXUSDT   = 'AVAXUSDT'
const.AXSUSDT    = 'AXSUSDT'
const.BCHUSDT    = 'BCHUSDT'
const.BNBUSDT    = 'BNBUSDT'
const.BTCUSDT    = 'BTCUSDT'
const.COMPUSDT   = 'COMPUSDT'
const.CRVUSDT    = 'CRVUSDT'
const.DASHUSDT   = 'DASHUSDT'
const.DOGEUSDT   = 'DOGEUSDT'
const.DOTUSDT    = 'DOTUSDT'
const.EOSUSDT    = 'EOSUSDT'
const.ETCUSDT    = 'ETCUSDT'
const.ETHUSDT    = 'ETHUSDT'
const.ICPUSDT    = 'ICPUSDT'
const.LINKUSDT   = 'LINKUSDT'
const.LTCUSDT    = 'LTCUSDT'
const.MATICUSDT  = 'MATICUSDT'
const.SUSHIUSDT  = 'SUSHIUSDT'
const.SOLUSDT    = 'SOLUSDT'
const.THETAUSDT  = 'THETAUSDT'
const.TRXUSDT    = 'TRXUSDT'
const.XRPUSDT    = 'XRPUSDT'
const.XEMUSDT    = 'XEMUSDT'
const.XLMUSDT    = 'XLMUSDT'
const.XTZUSDT    = 'XTZUSDT'
const.VETUSDT    = 'VETUSDT'
const.UNIUSDT    = 'UNIUSDT'

const.CURRENCIES = [
    const.AAVEUSDT,
    const.ADAUSDT,   # error 10001
    const.AVAXUSDT,  # error 10001
    const.AXSUSDT,
    const.BCHUSDT,
    const.BNBUSDT,
    const.BTCUSDT,   # error 35015 - low profit
    const.COMPUSDT,
    const.CRVUSDT,
    const.DASHUSDT,  # error 10001
    const.DOGEUSDT,
    const.DOTUSDT,
    const.EOSUSDT,
    const.ETCUSDT,
    const.ETHUSDT,
    const.ICPUSDT,
    const.LINKUSDT,
    const.LTCUSDT,
    const.MATICUSDT,  # error 10001
    const.SUSHIUSDT,
    const.SOLUSDT,
    const.THETAUSDT,
    const.TRXUSDT,
    const.UNIUSDT,
    const.XRPUSDT,   # error 10001
    const.XEMUSDT,
    const.XLMUSDT,
    const.XTZUSDT,   # error 130125 orderQty will be truncated to zero
    const.XTZUSDT,   # error 130125 orderQty will be truncated to zero
    const.VETUSDT
]

const.SUFFIX = 'equations'
const.ORDERS = 'orders'

# const.avg1_wnd = 31
# const.avg2_wnd = 127
# const.avg3_wnd = 63
# const.avg4_wnd = 255
# const.avg5_wnd = 3
# const.avg6_wnd = 3
# const.avg7_wnd = 3

# must be >= 31 ?  if wnd==15 => bad answers from bybit

const.avg1_wnd = 7
const.avg2_wnd = 3
const.avg3_wnd = 3
const.avg4_wnd = 3
const.avg5_wnd = 3
const.avg6_wnd = 3
const.avg7_wnd = 3

const.avg8_wnd = 31  # 127
const.avg_slow_wnd = 127  # 20v 25 30 35 40

const.max_ref_err_slow = 0.01
const.filter_min_ref_koef = 0.003
const.ER_wnd_size = 511

# 31->63,127->511
# 63 1023
# 63 300
# best 3, 7, 304%
# 7, 15 => 182%
# 15, 31 => 124%

const.check_extremum_wnd = 32

const.open_col_name = 'open'
const.close_col_name = 'close'

const.dt_col_name = 'dt'
const.value_col_name = 'value'
const.delta1_col_name = 'delta1'
const.delta2_col_name = 'delta2'
const.avg1_col_name = 'avg1'
const.avg2_col_name = 'avg2'
const.avg3_col_name = 'avg3'
const.avg4_col_name = 'avg4'
const.avg5_col_name = 'avg5'
const.avg6_col_name = 'avg6'
const.avg7_col_name = 'avg7'
const.avg8_col_name = 'avg8'
const.avg_fast_col_name = 'avg_fast'
const.avg_slow_col_name = 'avg_slow'
const.order_col_name = 'order'
const.order_profit_col_name = 'order_profit'

const.type_col_name = 'type'
const.open_ord_id_col_name = 'open_ord_id'
const.open_dt_col_name = 'open_dt'
const.open_price_col_name = 'open_price'
const.extremum_col_name = 'extremum'
const.extr_beg_col_name = 'extr_beg'
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

const.order_time_in_force_fill_or_kill = 'FillOrKill'
# OTHER VALUES NOT WORKS WITH SCALPING !!!
# const.order_time_in_force_good_till_cancel = 'GoodTillCancel'
# const.order_time_in_force_immediate_or_cancel = 'ImmediateOrCancel'
# const.order_time_in_force_post_only = 'PostOnly'

const.max_avg_err_wnd_size = 4
const.max_avg_error = 0.02
const.transit_max_pos = 11
const.transit_step = 0.1

const.select_best_wnd_size = 60
const.select_best_min_delta_prc = 3
const.select_best_max_mse_prc = 1.0  # 0.8
const.select_best_count = 4

const.one_curr_order_amount = 40.0

const.order_stop_lost_koef_buy = 0.975
const.order_stop_lost_koef_sell = 1.025

const.order_take_profit_koef_buy = 1.5
const.order_take_profit_koef_sell = 0.5

const.order_create_plus_koef_buy = 1.0001
const.order_create_plus_koef_sell = 0.9999

# |d3+d4| must be > (1% of price per 1 hour) = (1/60)*(price/100) = price * (1/6000))
# delta calulates per minute
# 1% per 1 hour = 1/60
# abs(d3 + d4) > price * 0.000167
# 0.0003
# 0.000075
# 0.00005
const.min_fast_avg_delta = 0.0001  # 0.0003
const.min_slow_avg_delta = 0.00001
const.max_backward_prc = 0.0  # 0.1
const.chain_fast_ref_profit = 0.025


