# trading
A bot for trading cryptocurrencies on Binance.

## Read this first
This project is currently in development and has bugs, poor error handling, and inconsistencies.

## Description
This is a simple spot trading bot that uses a trend-following strategy. It tracks all of the asset pairs of a primary asset such as USDT (examples include BTCUSDT, OGUSDT, ETHUSDT, etc.), and checks for an exponential rise in price. If the bot "thinks" (more on that below) that the price will keep rising, it places a buy order and a sell order at a higher price, typically 105% of the original price. If the price reaches that amount, the asset is sold, and profit is made. Otherwise, if the price drops too low, say 98% of the original price, a sell market order is instantly executed to prevent further losses.

## Implementation details
All of the bot's parameters, such as the profit margin, stop loss limit, and others, can be found in `asset.py` with some explanation. On a low level, the bot works as follows: A database is fed with data pulled from Binance. Assets are represented by a class called `Asset`, and all of the functional parts of the program exist within it. Each time an asset's price is updated, `_update_values` function subtracts the new price from the price of the asset `interval` seconds ago. The difference is then used to calculate `change`, how much % the asset price has changed. If `change` is greater than `change_threshold`, `counter` is increased by 1. If the price did not change or decreased, `counter` is reset to 0. If `counter` reaches `counter_threshold`, the program will interpret this as strong evidence of rising prices and run `_execute_trade` on a separate thread. The trading part is exactly as described in the "Description" section.

## Performance
Although the API is fully functional, and the database part is fine, there is still room for improvement to make the bot more efficient and effective. It has poor error handling, and sometimes an order fails due to price and lot size restrictions from Binance. As of now, because of these bugs, the bot has not made any profit and has only resulted in small losses.

Therefore, I would not recommend anyone to use it as it is. I created this project purely for fun because I am interested in finance and wanted to learn new things, but I'm a bit tired of it now, so I'm stepping back from it for the time being.

## Running on your device
1. Get your API Key and API Secret on the Binance website and save them in a `.env` file in the root folder.
2. Install all dependencies in `requirements.txt`.
3. Run `python feed_rest.py` or `python feed_ws.py`. They do the same thing, but one uses the Binance Rest API, while the other uses the Binance WebSocket.
4. Wait until the counter hits `INTERVAL`. You need to have some data in the database before running.
5. On another terminal window, run `python main.py`.

## Disclaimer
I am not responsible for any financial losses resulting from the bot. Use it at your own risk.