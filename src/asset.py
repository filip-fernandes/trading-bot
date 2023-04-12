import sqlalchemy
from database.model import MarketData
from sqlalchemy.orm import sessionmaker
import asyncio
from api import *


class Asset:

    def __init__(self, symbol, session, get_time, interval, threshold) -> None:
        self.symbol = symbol
        self.session = session
        self.t = get_time
        self.interval = interval
        self.threshold = threshold
        self.quantity = 0
        self.price = 0
        self.change = 0
        self.should_stop = True
        self.counter = 0 
   
    def get_change(self):
        t = self.t()
        assert self.interval < self.t()
        present = self.session.query(MarketData).filter(
            MarketData.close_time == t,
            MarketData.symbol == self.symbol
        ).all()[0]
        past = self.session.query(MarketData).filter(
            MarketData.close_time == t - self.interval, 
            MarketData.symbol == self.symbol
        ).all()[0]
        try:
            self.change = round(((present.last_price - past.last_price)/present.last_price) * 100, 2)
        except ZeroDivisionError:
            self.change = 0.0
        self.price = present

    def is_profitable(self):
        return self.counter > 3

    async def run(self):
        self.should_stop = False
        while True:
            self.get_change()
            if self.is_profitable():
                print(f'bought {self.symbol} at {self.price}')
                self.counter = 0
            if self.change > self.threshold:
                self.counter += 1
            else:
                self.counter = 0
            await asyncio.sleep(1)
        
class Controller:

    def __init__(self, threshold, interval, session) -> None:
        self.threshold = threshold
        self.interval = interval
        self.assets = [Asset(symbol, session, get_current_time, 10, self.threshold) for symbol in get_all_symbols("USDT")]
    
    async def run(self):
        tasks = [asset.run() for asset in self.assets]
        await asyncio.gather(*tasks)

engine = sqlalchemy.create_engine('sqlite:///MarketData.db')
Session = sessionmaker(bind=engine)
session = Session()

def get_current_time():
    return session.query(sqlalchemy.func.max(MarketData.close_time)).scalar()

async def main():
    con = Controller(1.0, 3.0, session)
    await con.run()

asyncio.run(main())
