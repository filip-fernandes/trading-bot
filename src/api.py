"""All http requests from the server are defined here"""
import requests
import time
import hmac
import hashlib
import requests
import time

URL = 'https://testnet.binance.vision/api/v3/'
API_KEY = 'NbDiqkIlHnd6f2AXBmzvQmmHPVbdlBYNFB34wHmmoukl7sTgl708nKg3CyG2yIac'
SECRET_KEY = b'yW0yASF4o2PEz1ae9y02JN7jk7nTBxId1X1Kw1SfM1VSE5oTlzMErwIWRrG0jScu'

def execute_request(endpoint, method="GET", params=None, public=True) -> dict:
    url = URL + endpoint
    # public requests are always GET
    if public:
        res = requests.get(url, params=params)
    else:
        # Add the time to the parameters
        params['timestamp'] = int(time.time() * 1000) 
        # Generate the signature
        query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
        signature = hmac.new(SECRET_KEY, query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        # Add the signature to the parameters
        params['signature'] = signature
        # Send the request
        headers = {'X-MBX-APIKEY': API_KEY}
        if method == "GET":
            res = requests.get(url, headers=headers, params=params)
        else:
            res = requests.post(url, headers=headers, data=params)
    status_code, content = res.status_code, res.json()
    return status_code, content

# Public Part

def get_all_symbols(primary) -> list:
    endpoint = 'ticker/price'
    _, content = execute_request(endpoint)
    symbols = [item['symbol'] for item in content if primary in item["symbol"]]
    return symbols

def get_24hr(primary) -> list:
    endpoint = 'ticker/24hr'
    _, content = execute_request(endpoint)
    tickers = [item for item in content if primary in item["symbol"]]
    return tickers

def get_number_of_symbols(primary) -> list:
    endpoint = 'ticker/price'
    _, content = execute_request(endpoint)
    number = len([item for item in content if primary in item["symbol"]])
    return number


# Private Part
def new_order(symbol, side, type, quantity, price=0.0) -> dict:
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
    status_code, content  = execute_request(endpoint, "POST", params, public=False)
    if status_code != 200:
        return False
    return True

def get_order(symbol) -> dict:
    endpoint = 'openOrders'
    params = {
        'symbol': symbol,
    }
    status_code, content = execute_request(endpoint, "GET", params, public=False)
    if status_code != 200:
        return False
    status = content[0]['status']
    if status == "NEW":
        return False
    return True
  



