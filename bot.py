from credentials import API_KEY, SECRET_KEY
from binance.spot import Spot
import http

client = Spot()

# Get server timestamp
print(client.time())
# Get klines of BTCUSDT at 1m interval
#print(client.klines("BTCUSDT", "1m", limit=5))


# API key/secret are required for user data endpoints
client = Spot(api_key=API_KEY, api_secret=SECRET_KEY)

