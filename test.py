from client_bybit import *

# Not forget change price

exists1 = client_position_check(const.order_side_buy, const.XTZUSDT)
exists2 = client_position_check(const.order_side_sell, const.XTZUSDT)

success1, order_id, time_now, qty, qty_in_usd, price = client_position_open(const.order_side_buy, const.XTZUSDT, 4, 5.666)
exists3 = client_position_check(const.order_side_buy, const.XTZUSDT)
exists4 = client_position_check(const.order_side_sell, const.XTZUSDT)
success1, order_id, time_now, qty, qty_in_usd, price = client_position_close(const.order_side_buy, const.XTZUSDT, 4, 5.666)

exists5 = client_position_check(const.order_side_buy, const.XTZUSDT)
exists6 = client_position_check(const.order_side_sell, const.XTZUSDT)


success3, order_id, time_now, qty, qty_in_usd, price = client_position_open(const.order_side_sell, const.XTZUSDT, 3, 5.666)
exists7 = client_position_check(const.order_side_buy, const.XTZUSDT)
exists8 = client_position_check(const.order_side_sell, const.XTZUSDT)
success4, order_id, time_now, qty, qty_in_usd, price = client_position_close(const.order_side_sell, const.XTZUSDT, 3, 5.666)

exists9 = client_position_check(const.order_side_buy, const.XTZUSDT)
exists10 = client_position_check(const.order_side_sell, const.XTZUSDT)
sum=0.0
