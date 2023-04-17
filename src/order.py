from api import PrivateAPI, PublicAPI

class Order:
    def __init__(self, symbol: str, side: str, type: str, quantity: float, price: float) -> None:
        self.api = PrivateAPI()
        data = self.api.new_order(symbol, side, type, quantity, price)
        self.symbol = symbol
        self.order_id = float(data["content"]["orderId"])
        self.quantity = float(data["content"]["origQty"])
        self.price = float(data["content"]["price"])
    
    def cancel(self) -> None:
        response = self.api.cancel_order(self.symbol, self.order_id)
        if response["content"]["status"] == "CANCELED":
            return True
        return False
        
    def was_fullfiled(self) -> bool:
        response = self.api.get_order(self.symbol, self.order_id)
        if response["content"]["status"] == "FILLED":
            return True
        return False

        




