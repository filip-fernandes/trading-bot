import asyncio
import threading
from database.db_utils import *
from api import *


class Asset:

    def __init__(self, symbol, interval, threshold) -> None:
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
        return self.counter > 3

    async def run(self):
        self.should_stop = False
        while True:
            self.update_change()
            if self.is_profitable():
                print(f'bought {self.symbol} at {self.price}')
                self.counter = 0
            if self.change > self.threshold:
                self.counter += 1
            else:
                self.counter = 0
            await asyncio.sleep(1)
    
    def execute_trade(self):
        # separate into a thread
        # get precise information
        #
        pass

        
class Controller:

    def __init__(self, threshold, interval, primary) -> None:
        self.assets = [Asset(symbol, interval, threshold) for symbol in get_all_symbols(primary)]
    
    async def run(self):
        tasks = [asset.run() for asset in self.assets]
        await asyncio.gather(*tasks)

    def balance(self):
        pass


async def main():
    con = Controller(0.1, 2.0, "USDT")
    await con.run() 

asyncio.run(main())