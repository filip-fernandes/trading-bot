"""All http requests from the server are defined here"""
import requests


URL = 'https://api.binance.com/api/v3/'

def execute_request(endpoint) -> dict:
    res = requests.get(URL + endpoint)
    return res.json()

def get_all_symbols(primary) -> list:
    endpoint = 'ticker/price'
    res = execute_request(endpoint)
    symbols = [item['symbol'] for item in res if primary in item["symbol"]]
    return symbols

def get_24hr(primary) -> list:
    endpoint = 'ticker/24hr'
    res = execute_request(endpoint)
    tickers = [item for item in res if primary in item["symbol"]]
    return tickers

def get_number_of_symbols(primary) -> list:
    endpoint = 'ticker/price'
    res = execute_request(endpoint)
    number = len([item for item in res if primary in item["symbol"]])
    return number