from order import Order
import sys
from api import PrivateAPI
import time
from pprint import pprint


api = PrivateAPI("BTCUSDT")

#print(api.new_order("BUY", "MARKET", 0.001))

print(api.get_balance())