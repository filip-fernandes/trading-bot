import asyncio
import websockets
import json
from api import PublicAPI
from database.model import MarketData
from database.db_utils import (
    add_to_db,
    get_num_batches,
    delete_old_data,
)


async def binance_ws(primary: str) -> None:
    """
    Feed the database using the binance websocket 
    """
    # Populate the last_prices dict 
    all_symbols = PublicAPI.get_all_symbols(primary)
    past_tickers = PublicAPI.get_tickers(primary)
    last_prices = {}
    for ticker in past_tickers:
        last_prices[ticker["symbol"]] = ticker["price"]

    uri = "wss://stream.binance.com:9443/ws/!ticker_1h@arr"

    curr_time = 0

    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            message = json.loads(message)
            tickers = {}
            for ticker in message:
                if primary in ticker["s"]:
                    tickers[ticker["s"]] = ticker
            not_included = set(all_symbols) - set(tickers.keys())
            data = []
            for symbol_ in all_symbols:
                # add all the symbols data. if the symbols ins't included in this particular message,
                # add its last price instead
                if symbol_ in not_included:
                    last_price = last_prices[symbol_]
                else:
                    last_price = tickers[symbol_]["c"]
                last_prices[symbol_] = last_price
                symbol = symbol_
                close_time = curr_time
                data.append(MarketData(symbol=symbol, last_price=last_price, close_time=close_time))

            add_to_db(data)
            # Query the database for the number of distinct time values
            num_batches = get_num_batches()

            # Crop the db to maximum size
            if num_batches >= 90:
                delete_old_data()

            curr_time += 1
            print(curr_time)

            
if __name__ == "__main__":
    PRIMARY = "USDT"
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(binance_ws(PRIMARY))
