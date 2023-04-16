""" Feed the database"""
from database.model import MarketData
from database.db_utils import (
    add_to_db,
    get_num_batches,
    delete_old_data
)
from api import get_24hr
import time


def main():
    MAX_BATCHES = 60
    RATE = 5
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
        add_to_db(data)
        curr_time += 1

        # Query the database for the number of distinct time values
        num_batches = get_num_batches()

        # Crop the db to maximum size
        if num_batches > MAX_BATCHES:
            delete_old_data()
            curr_time = 0

        time.sleep(RATE)
                

if __name__ == '__main__':
    main()