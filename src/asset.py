import threading
from database.db_utils import *
from api import Client
import time

class Asset:

    def __init__(self, symbol, interval, threshold) -> None:
        self.client = Client()
        self.symbol = symbol
        self.interval = interval
        self.threshold = threshold
        self.quantity = 0
        self.price = 0
        self.change = 0
        self.should_stop = True
        self.counter = 0
   
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
        self.execute_trade()
        if self.is_profitable():
            self.execute_trade()
            self.counter = 0
            #return self
        if self.change > self.threshold:
            self.counter += 1
        else:
            self.counter = 0
    
    def execute_trade(self):
        # separate into a thread
        # get precise information
        print(f'bought {self.symbol} at {self.price}')
        
