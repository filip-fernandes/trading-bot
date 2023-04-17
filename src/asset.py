import threading
from database.db_utils import *
import time
from order import Order
from api import PrivateAPI

class Asset:

    def __init__(self, symbol, interval, threshold) -> None:
        self.symbol = symbol
        self.interval = interval
        self.threshold = threshold
        self.price = 0
        self.change = 0
        self.counter = 0
        self.spendable = 0
   
    def update_values(self):
        t = get_current_time()
        assert self.interval < t
        present = get_data(self.symbol, t)
        past =  get_data(self.symbol, t, self.interval)
        try:
            self.change = round(((present.last_price - past.last_price)/present.last_price) * 100, 2)
        except ZeroDivisionError:
            self.change = 0.0
        self.price = round(present.last_price, 2)

    def is_profitable(self):
        return self.change > self.threshold

    def run(self):
        self.update_values()
        thread = threading.Thread(target=self.execute_trade)
        thread.start()
        return
        if self.is_profitable():
            self.execute_trade()
            self.counter = 0
            #return self
        if self.change > self.threshold:
            self.counter += 1
        else:
            self.counter = 0
    
    def execute_trade(self):
        chunk = 0.1 * self.spendable
        quantity = round(chunk / self.price, 2)
        buy_order = Order(
            symbol=self.symbol,
            side="BUY",
            type="LIMIT",
            quantity=quantity,
            price=self.price
        )
        while True:
            if not buy_order.was_fullfiled():
                continue
            initial_capital = buy_order.quantity * buy_order.price
            time.sleep(5)
            sell_order = Order(
                symbol=self.symbol,
                side="SELL",
                type="LIMIT",
                quantity=quantity,
                price=self.price
            )   
            if sell_order.was_fullfiled():
                final_capital = sell_order.quantity * sell_order.price
                print(f'profit of {initial_capital - final_capital}')
                break
        self.spendable -= chunk


    
        
