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
URL = 'https://api.binance.com/api/v3/'

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
        status_code, content = execute_request(endpoint,  {}, "GET", True)
        assert status_code == 200, f"Error: {content}"
        symbols = [item['symbol'] for item in content if primary in item["symbol"]]
        return symbols

    @staticmethod
    def get_tickers(primary: str) -> list:
        """
        Get ticker data for a given primary currency
        """
        endpoint = 'ticker/price'
        status_code, content = execute_request(endpoint,  {}, "GET", True)
        assert status_code == 200, f"Error: {content}"
        tickers = [item for item in content if primary in item["symbol"]]
        return tickers

    @staticmethod
    def get_number_of_symbols(primary: str) -> int:
        """
        Get the number of symbols for a given primary currency
        """
        endpoint = 'ticker/price'
        status_code, content = execute_request(endpoint,  {}, "GET", True)
        assert status_code == 200, f"Error: {content}"
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
        status_code, content = execute_request(endpoint, params, "GET", True)
        assert status_code == 200, f"Error: {content}"
        filter_list = [content["symbols"][0]['filters'][i] for i in range(2)]
        filters = {
            "min_price": float(filter_list[0]['minPrice']),
            "min_qty": float(filter_list[1]['minQty']),
            "step_size": float(filter_list[1]['stepSize'])
        }
        return filters

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
        assert status_code == 200, f"Error: {content}"
        response = {
            "order_id": int(content['orderId']), 
            "price": float(content["price"]),
            "quantity": float(content["origQty"]),
        }
        return response

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
        assert status_code == 200, f"Error: {content}"
        response = content['status']
        return response
    
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
        assert status_code == 200, f"Error: {content}"
        response = content['status']
        return response
    
    @staticmethod
    def get_balance(primary) -> str:
        """
        Get the balance of the account for a given symbol
        """
        endpoint = 'account'
        status_code, content = execute_request(endpoint, {}, "GET", False)
        assert status_code == 200, f"Error: {content}"
        balance = [item["free"] for item in content["balances"] if item["asset"] == primary]
        response = float(balance[0])
        return response

