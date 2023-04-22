import asyncio
import websockets
import json
from pprint import pprint

async def binance_ws():
    uri = "wss://stream.binance.com:9443/ws/!miniTicker@arr"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            message = json.loads(message)
            tickers = [ticker for ticker in message if "USDT" in ticker["s"]]
            pprint(len(tickers))

asyncio.get_event_loop().run_until_complete(binance_ws())