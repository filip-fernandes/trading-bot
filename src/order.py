from api import PrivateAPI

class Order:
    def __init__(self, symbol: str, side: str, type: str, quantity: float, price: float) -> None:
        self.api = PrivateAPI(symbol)
        response = self.api.new_order(side, type, quantity, price)
        try:
            assert response["status code"] == 200
        except AssertionError:
            raise AssertionError(response["content"])
        self.symbol = symbol
        self.order_id = int(response["content"]["orderId"])
        self.quantity = float(response["content"]["origQty"])
        self.price = float(response["content"]["price"])
    
    def cancel(self) -> None:
        response = self.api.cancel_order(self.order_id)
        try:
            assert response["status code"] == 200
        except AssertionError:
            raise AssertionError(response["content"])
        
        if response["content"]["status"] == "CANCELED":
            return True
        return False
        
    def was_fullfiled(self) -> bool:
        response = self.api.get_order(self.order_id)
        try:
            assert response["status code"] == 200
        except AssertionError:
            raise AssertionError(response["content"])
        
        if response["content"]["status"] == "FILLED":
            return True
        return False

        




