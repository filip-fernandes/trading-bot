""" Feed the database"""
from database.model import MarketData
from database.db_utils import (
    add_to_db,
    get_num_batches,
    delete_old_data
)
from api import PublicAPI

curr_time = 0     # representative time, not real-world time
MAX_BATCHES = 100 # max time that the db stores = MAX_BATCHES * RATE

def feed(primary):
    
    global curr_time
    tickers = PublicAPI.get_24hr(primary)
    data = []
    for ticker in tickers:
        symbol = ticker["symbol"]
        last_price = ticker["lastPrice"]
        close_time = curr_time
        data.append(MarketData(symbol=symbol, last_price=last_price, close_time=close_time))
    add_to_db(data)
    curr_time += 1

    # Query the database for the number of distinct time values
    num_batches = get_num_batches()

    # Crop the db to maximum size
    if num_batches >= MAX_BATCHES:
        delete_old_data()
    
    print(curr_time)

            