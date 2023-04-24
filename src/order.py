from api import PrivateAPI


class Order:

    def __init__(self, symbol: str, side: str, type: str, quantity: float, price: float = 0.0) -> None:
        self.api = PrivateAPI(symbol)
        response = self.api.new_order(side, type, quantity, price)
        self.symbol = symbol
        self.order_id = response["order_id"]
        self.quantity = response["quantity"]
        self.price = response["price"]
    
    def cancel(self) -> bool:
        status = self.api.cancel_order(self.order_id)
        if status == "CANCELED":
            return True
        return False
        
    def was_fullfiled(self) -> bool:
        status = self.api.get_order(self.order_id)
        if status == "FILLED":
            return True
        return False


        




