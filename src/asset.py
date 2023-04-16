import threading
from database.db_utils import *
import time
from api import new_order, cancel_order, get_order

class Asset:

    def __init__(self, symbol, interval, threshold) -> None:
        self.symbol = symbol
        self.interval = interval
        self.threshold = threshold
        self.quantity = 0
        self.price = 0
        self.change = 0
        self.counter = 0
        self.spendable = 0
   
    def update_change(self):
        t = get_current_time()
        assert self.interval < t
        present = get_data(self.symbol, t)
        past =  get_data(self.symbol, t, self.interval)
        try:
            self.change = round(((present.last_price - past.last_price)/present.last_price) * 100, 2)
        except ZeroDivisionError:
            self.change = 0.0
        self.price = present.last_price

    def is_profitable(self):
        return self.change > self.threshold

    def run(self):
        self.update_change()
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
        self.quantity = round(chunk / self.price, 2)
        self.price = round(self.price, 2)
        order = new_order(self.symbol, "BUY", "LIMIT", self.quantity, self.price)
        if order:
            print(f'bought {self.symbol} at {self.price}')
            if not get_order(self.symbol):
                cancelled = cancel_order(self.symbol)
                if cancelled:
                    print(f'cancelled {self.symbol}')
            sold = new_order(self.symbol, "SELL", "MARKET", self.quantity)
            if sold:
                print(f"SOLD {self.symbol}")
        else:
            print(self.quantity, self.price, self.symbol)
        self.quantity = 0

    
        
