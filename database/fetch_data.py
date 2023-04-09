from model import MarketData, Base
from API import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time as t
 
engine = create_engine('sqlite:///MarketData.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

while True:
    tickers = get_24hr()
    data = []
    for ticker in tickers:
        symbol = ticker["symbol"]
        price = ticker["lastPrice"]
        time = ticker["closeTime"]
        data.append(MarketData(symbol=symbol, price=price, time=time))
    session.add_all(data)
    session.commit()
    t.sleep(1.0)
        