from model import MarketData, Base
from API import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time
import os

def delete_db():
    os.remove('MarketData.db')

os.remove('MarketData.db')
engine = create_engine('sqlite:///MarketData.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

curr_time = 0
rate = 5 # 5 seconds

while True:
    tickers = get_24hr()
    data = []
    for ticker in tickers:
        symbol = ticker["symbol"]
        last_price = ticker["lastPrice"]
        close_time = curr_time
        data.append(MarketData(symbol=symbol, last_price=last_price, close_time=close_time))
    session.add_all(data)
    session.commit()
    curr_time += 1
    time.sleep(rate)
        