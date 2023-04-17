"""All http requests from the server are defined here"""
import requests
import time
import hmac
import hashlib
import requests
import time
import os
from dotenv import load_dotenv


class API:

    def __init__(self) -> None:
        load_dotenv() 
        self.API_KEY = os.getenv('API_KEY').encode()
        self.SECRET_KEY = os.getenv('API_SECRET').encode()
        self.URL = 'https://testnet.binance.vision/api/v3/'
        
    def execute_request(self, endpoint: str, params: dict, method: str, 
    public: bool) -> tuple:
        """
        Execute a request to the server
        """
        url = f"{self.URL}{endpoint}"
        if not params:
            params = {}
        if not public:
            params['timestamp'] = int(time.time() * 1000) 
            query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
            signature = hmac.new(self.SECRET_KEY, query_string.encode('utf-8'), hashlib.sha256).hexdigest()
            params['signature'] = signature
            headers = {'X-MBX-APIKEY': self.API_KEY}
            response = requests.request(method, url, headers=headers, params=params)
        else:
            # public requests are always GET
            response = requests.get(url, params=params)
        status_code = response.status_code
        content =  response.json()
        return status_code, content


class PublicAPI(API):

    def __init__(self):
        super().__init__()

    def execute_request(self, endpoint: str, params: dict = None) -> tuple:
        return super().execute_request(endpoint, params, method = "GET", public = True)

    def get_all_symbols(self, primary: str) -> list:
        """
        Get all symbols for a given primary currency
        """
        endpoint = 'ticker/price'
        _, content = self.execute_request(endpoint)
        symbols = [item['symbol'] for item in content if primary in item["symbol"]]
        return symbols

    def get_24hr(self, primary: str) -> list:
        """
        Get 24hr data for a given primary currency
        """
        endpoint = 'ticker/24hr'
        _, content = self.execute_request(endpoint)
        tickers = [item for item in content if primary in item["symbol"]]
        return tickers

    def get_number_of_symbols(self, primary: str) -> int:
        """
        Get the number of symbols for a given primary currency
        """
        endpoint = 'ticker/price'
        _, content = self.execute_request(endpoint)
        number = len([item for item in content if primary in item["symbol"]])
        return number

    def get_filters(self, symbol: str = None):
        """
        Get the exchange info for a given symbol
        """
        endpoint = 'exchangeInfo'
        params = {
            'symbol': symbol,
        }
        _, content = self.execute_request(endpoint, params)
        return content


class PrivateAPI(API):

    def __init__(self) -> None:
        super().__init__()

    def execute_request(self, endpoint: str, method, params: dict = None) -> tuple:
        return super().execute_request(endpoint, params, method, public=False)

    def new_order(self, symbol: str, side: str, type: str, quantity: float, 
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
        status_code, content  = self.execute_request(endpoint, "POST", params)
        return {"status code": status_code, "content": content}

    def get_order(self, symbol: str, order_id: int) -> bool:
        """
        Check if the order is filled for a given symbol
        """
        endpoint = 'order'
        params = {
            'symbol': symbol,
            'orderId': order_id,
        }
        status_code, content =  self.execute_request(endpoint, "GET", params)
        return {"status code": status_code, "content": content}
    
    def get_balance(self, symbol: str) -> str:
        """
        Get the balance of the account for a given symbol
        """
        endpoint = 'account'
        status_code, content = self.execute_request(endpoint, method="GET")
        balance = [item["free"] for item in content["balances"] if item["asset"] == symbol]
        return {"status code": status_code, "content": balance}

    def cancel_order(self, symbol: str, order_id: int) -> bool:
        """
        Cancel the order of a given symbol
        """
        endpoint = 'order'
        params = {
            'symbol': symbol,
            'orderId': order_id,
        }
        status_code, content = self.execute_request(endpoint, "DELETE", params)
        return {"status code": status_code, "content": content}