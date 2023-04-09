import requests


URL = 'https://api.binance.com/api/v3/'

def execute_request(endpoint):
    res = requests.get(URL + endpoint)
    return res.json()

def get_all_symbols():
    endpoint = 'ticker/price'
    res = execute_request(endpoint)
    symbols = [item['symbol'] for item in res]
    return symbols

def get_24hr():
    endpoint = 'ticker/24hr'
    res = execute_request(endpoint)
    res = [item for item in res if "USDT" in item["symbol"]]
    return res
