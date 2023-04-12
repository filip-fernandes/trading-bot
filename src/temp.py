import sqlalchemy
from database.model import MarketData
from sqlalchemy.orm import sessionmaker
import threading
from api import *
import concurrent.futures

c = 0

class Asset:

    def __init__(self, symbol, threshold) -> None:
        self.symbol = symbol
        self.quantity = 0
        self.price = 0
        self.threshold = threshold
        self.change = 0
        self.c = 0
   
    def hot_tokens(self):
        pass
    
    def execute_order(self):
        pass

    def is_profitable(self):
        return self.change > self.threshold

    def __call__(self):
        self.should_stop = False
        for _ in range(1000):
            if self.is_profitable():
                print(self.symbol, self.change)
            global c
            c += 1
        print("executed", self.symbol)
        


engine = sqlalchemy.create_engine('sqlite:///MarketData.db')
Session = sessionmaker(bind=engine)
session = Session()

def get_current_time():
    return session.query(MarketData).all()[-1].close_time

assets = []

symbs = get_all_symbols("USDT")
for s in symbs:
    assets.append(Asset(symbol=s, threshold=1.3))

# Create a thread pool with a maximum of 100 threads
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    # Submit the __call__() method of each Asset object to the thread pool
    futures = [executor.submit(asset.__call__) for asset in assets]
    # Wait for all futures to finish
    concurrent.futures.wait(futures)

print(c)