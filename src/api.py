"""All http requests from the server are defined here"""
import requests
import time
import hmac
import hashlib
import requests
import time
import os
from dotenv import load_dotenv


load_dotenv() 
API_KEY = os.getenv('API_KEY').encode()
SECRET_KEY = os.getenv('API_SECRET').encode()
URL = 'https://testnet.binance.vision/api/v3/'

def execute_request(endpoint: str, params: dict = None, method: str = "GET", 
    public: bool = True) -> tuple:
    """
    Execute a request to the server
    """
    url = f"{URL}{endpoint}"
    if not params:
        params = {}
    if not public:
        params['timestamp'] = int(time.time() * 1000) 
        query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
        signature = hmac.new(SECRET_KEY, query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        params['signature'] = signature
        headers = {'X-MBX-APIKEY': API_KEY}
        response = requests.request(method, url, headers=headers, params=params)
    else:
        # public requests are always GET
        response = requests.get(url, params=params)
    status_code = response.status_code
    content =  response.json()
    return status_code, content

# Public Part

def get_all_symbols(primary: str) -> list:
    """
    Get all symbols for a given primary currency
    """
    endpoint = 'ticker/price'
    _, content = execute_request(endpoint)
    symbols = [item['symbol'] for item in content if primary in item["symbol"]]
    return symbols

def get_24hr(primary: str) -> list:
    """
    Get 24hr data for a given primary currency
    """
    endpoint = 'ticker/24hr'
    _, content = execute_request(endpoint)
    tickers = [item for item in content if primary in item["symbol"]]
    return tickers

def get_number_of_symbols(primary: str) -> int:
    """
    Get the number of symbols for a given primary currency
    """
    endpoint = 'ticker/price'
    _, content = execute_request(endpoint)
    number = len([item for item in content if primary in item["symbol"]])
    return number

def get_filters(symbol: str = None):
    """
    Get the exchange info for a given symbol
    """
    endpoint = 'exchangeInfo'
    params = {
        'symbol': symbol,
    }
    _, content = execute_request(endpoint, params)
    return content


# Private Part
def new_order(symbol: str, side: str, type: str, quantity: float, 
    price: float = 0.0) -> bool:
    """
    Place a new order for a given symbol
    """
    endpoint = 'order'
    params = {
        'symbol': symbol,
        'side': side,
        'type': type,
        'quantity': quantity,
    }
    if params['type'] == "LIMIT":
        params['price'] = price
        params['timeInForce'] = 'GTC'
    status_code, content  = execute_request(endpoint, params, "POST", False)
    if status_code != 200:
        print(content,  "NEW ORDER FAILURE")
        return False
    return True

def get_order(symbol: str) -> bool:
    """
    Check if the order is filled for a given symbol
    """
    endpoint = 'openOrders'
    params = {
        'symbol': symbol,
    }
    status_code, content = execute_request(endpoint, params, "GET", False)
    if status_code != 200 or not content:
        return False
    status = content[0]['status']
    if status == "FILLED":
        return True
    return False
  
def get_balance(symbol: str = "USDT") -> str:
    """
    Get the balance of the account for a given symbol
    """
    endpoint = 'account'
    status_code, content = execute_request(endpoint, method="GET", public=False)

    if status_code != 200:
        print(content, "GET BALANCE FAILURE")
        return status_code
    
    balance = [item["free"] for item in content["balances"] if item["asset"] == symbol][0]

    return float(balance)

def cancel_order(symbol: str) -> bool:
    """
    Cancel the order of a given symbol
    """
    endpoint = 'openOrders'
    params = {
        'symbol': symbol,
    }
    status_code, content = execute_request(endpoint, params, "DELETE", False)
    
    if status_code != 200:
        print(content, "CANCEL ORDER FAILURE")
        return False
    return True


