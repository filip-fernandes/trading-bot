"""All http requests from the server are defined here"""
import requests
import time
import hmac
import hashlib
import os
from dotenv import load_dotenv


load_dotenv() 
API_KEY = os.getenv('API_KEY').encode()
SECRET_KEY = os.getenv('API_SECRET').encode()
URL = 'https://testnet.binance.vision/api/v3/'

def execute_request(endpoint: str, params: dict, method: str, 
public: bool) -> tuple:
    """
    Execute a request to the server
    """
    url = f"{URL}{endpoint}"
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
    content = response.json()
    return status_code, content


class PublicAPI:
     
    @staticmethod
    def get_all_symbols(primary: str) -> list:
        """
        Get all symbols for a given primary currency
        """
        endpoint = 'ticker/price'
        _, content = execute_request(endpoint,  {}, "GET", True)
        symbols = [item['symbol'] for item in content if primary in item["symbol"]]
        return symbols

    @staticmethod
    def get_24hr(primary: str) -> list:
        """
        Get 24hr data for a given primary currency
        """
        endpoint = 'ticker/24hr'
        _, content = execute_request(endpoint,  {}, "GET", True)
        tickers = [item for item in content if primary in item["symbol"]]
        return tickers

    @staticmethod
    def get_number_of_symbols(primary: str) -> int:
        """
        Get the number of symbols for a given primary currency
        """
        endpoint = 'ticker/price'
        _, content = execute_request(endpoint,  {}, "GET", True)
        number = len([item for item in content if primary in item["symbol"]])
        return number

    @staticmethod
    def get_filters(symbol: str = None):
        """
        Get the exchange info for a given symbol
        """
        endpoint = 'exchangeInfo'
        params = {
            'symbol': symbol,
        }
        _, content = execute_request(endpoint, params, "GET", True)
        return content

class PrivateAPI:

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    def new_order(self, side: str, type: str, quantity: float, 
        price: float = 0.0) -> bool:
        """
        Place a new order for a given symbol
        """
        endpoint = 'order'
        params = {
            'symbol': self.symbol,
            'side': side,
            'type': type,
            'quantity': quantity,
        }
        if params['type'] == "LIMIT":
            params['price'] = price
            params['timeInForce'] = 'GTC'
        status_code, content  = execute_request(endpoint, params, "POST", False)
        return {"status code": status_code, "content": content}

    def get_order(self, order_id: int) -> bool:
        """
        Check if the order is filled for a given symbol
        """
        endpoint = 'order'
        params = {
            'symbol': self.symbol,
            'orderId': order_id,
        }
        status_code, content =  execute_request(endpoint, params, "GET", False)
        return {"status code": status_code, "content": content}
    
    def cancel_order(self, order_id: int) -> bool:
        """
        Cancel the order of a given symbol
        """
        endpoint = 'order'
        params = {
            'symbol': self.symbol,
            'orderId': order_id,
        }
        status_code, content = execute_request(endpoint, params, "DELETE", False)
        return {"status code": status_code, "content": content}
    
    @staticmethod
    def get_balance(primary) -> str:
        """
        Get the balance of the account for a given symbol
        """
        endpoint = 'account'
        status_code, content = execute_request(endpoint, {}, "GET", False)
        balance = [item["free"] for item in content["balances"] if item["asset"] == primary]
        return {"status code": status_code, "content": balance}

