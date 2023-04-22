from api import PublicAPI, PrivateAPI
from order import Order
from asset import Asset
from database.db_utils import get_data, get_current_time
import time
import math
from pprint import pprint

# t = get_current_time()
# price = get_data("OGUSDT", t).last_price
# old_money = PrivateAPI.get_balance(primary="USDT")["balance"] 
# print(old_money/price)
# quant = math.floor(((old_money/price) * 10))/10
# print(quant, price)
# def trade():
#     print("buying...")
#     ord = Order(symbol="OGUSDT", side="BUY", type="LIMIT", quantity=quant, price=price)
#     print("bought")
#     while not ord.was_fullfiled():
#         continue
#     print("order fulfilled, buy")
#     while not get_data("OGUSDT", get_current_time()).last_price >= price * 1.03:
#         if get_data("OGUSDT", get_current_time()).last_price <= price * 0.98:
#             new_ord = Order(symbol="OGUSDT", side="SELL", type="MARKET", quantity=quant)
#             if new_ord.was_fullfiled():
#                 print("order fulfilled, sell")
#             print("price too low")
#             new_money = PrivateAPI.get_balance(primary="USDT")["balance"]
#             print(round((new_money - old_money) * 4.94, 2))
#             return
#         continue
#     print(quant, ord.quantity)
#     new_ord = Order(symbol="OGUSDT", side="SELL", type="MARKET", quantity=quant)
#     if new_ord.was_fullfiled():
#         print("order fulfilled, sell")

#     new_money = PrivateAPI.get_balance(primary="USDT")["balance"]
#     print(round((new_money - old_money) * 4.94, 2))



# trade()

pprint(PublicAPI.get_filters("OGUSDT"))

asset = Asset("OGUSDT", 1, 2, 3, 1, 1, 50)
print(asset._get_quantity())