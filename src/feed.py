# Feed the database 

from database.model import MarketData, Base
from api import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time
import os

os.remove('MarketData.db')
engine = create_engine('sqlite:///MarketData.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Define the maximum number of batches
MAX_BATCHES = 300
RATE = 5 # 5 seconds
curr_time = 0

while True:
    # append batches of MarketData
    tickers = get_24hr("USDT")
    data = []
    for ticker in tickers:
        symbol = ticker["symbol"]
        last_price = ticker["lastPrice"]
        close_time = curr_time
        data.append(MarketData(symbol=symbol, last_price=last_price, close_time=close_time))
    session.add_all(data)
    session.commit()
    curr_time += 1

    # Query the database for the number of distinct time values
    num_batches = session.query(MarketData.close_time.distinct()).count()

    # Crop the db to maximum size
    if num_batches > MAX_BATCHES:
        oldest_time = session.query(MarketData.close_time.distinct()).order_by(MarketData.close_time).first()[0]
        session.query(MarketData).filter(MarketData.close_time == oldest_time).delete()
        session.commit()

    time.sleep(RATE)
            