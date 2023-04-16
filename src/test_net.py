from api import new_order, get_order, get_balance, cancel_order, get_24hr, exchange_info
import sys
import time
from pprint import pprint


print(get_balance("USDT"))

pprint(exchange_info("BTCUSDT"))
