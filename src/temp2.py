import sqlalchemy
from database.model import MarketData
from sqlalchemy.orm import sessionmaker
import threading
from api import *
import concurrent.futures

class Asset:

    def __init__(self, symbol, threshold) -> None:
        self.symbol = symbol
        self.threshold = threshold
        self.quantity = 0
        self.price = 0
        self.change = 0
        self.counter = 0

    def is_profitable(self):
        return self.counter > 3

    def run(self):
        self.should_stop = False
        if self.is_profitable():
            print(f'bought {self.symbol} at {self.price}')
            self.counter = 0
        if self.change > self.threshold:
            self.counter += 1
        else:
            self.counter = 0
    
    def execute_order(self):
        pass
        

class Controller:

    def __init__(self, threshold, interval) -> None:
        self.threshold = threshold
        self.interval = interval
        self.assets = [Asset(symbol, self.threshold) for symbol in get_all_symbols("USDT")]
        
    def get_data(self):
        assert self.interval < self.get_current_time()
        t = self.get_current_time()
        batch_present = session.query(MarketData).filter(MarketData.close_time == t).all()
        batch_past = session.query(MarketData).filter(MarketData.close_time == t - self.interval).all()
        current_data = [{"symbol": item.symbol,
                         "price": item.last_price} for item in batch_present]
        past_data =  [{"symbol": item.symbol,
                        "price": item.last_price} for item in batch_past]
        for present, past in zip(current_data, past_data):
            try:
                change = round(((present["price"] - past["price"])/present["price"]) * 100, 2)
            except ZeroDivisionError:
                change = 0.0
            for asset in self.assets:
                if asset.symbol == present["symbol"]:
                    asset.change = change
                    asset.price = present["price"]
                    asset.run()
                    break

    def get_current_time(self):
        return session.query(MarketData).all()[-1].close_time
    
    def run(self):
        t = self.get_current_time()
        while True:
            if t != self.get_current_time:
                self.get_data()
                t = self.get_current_time()

engine = sqlalchemy.create_engine('sqlite:///MarketData.db')
Session = sessionmaker(bind=engine)
session = Session()


con = Controller(1.5, 15.0)
con.run()



# symbs = get_all_symbols("USDT")
# for s in symbs:
#     assets.append(Asset(symbol=s, threshold=1.3))

# # Create a thread pool with a maximum of 100 threads


