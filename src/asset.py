import threading
from database.db_utils import get_data
import math
from order import Order
from api import PrivateAPI

"""
THIS CODE HAS BUGS, BE CAREFUL. I strongly advice testing it or fixing the bugs on the Test API.

To fix:
    self.rules -> these values below are generic and does not comply with all of the assets

To add:
    I'm not calculating any of the taxes that Binance imposes. Would be better that was accounted when
    trading.
"""

class Asset:

    def __init__(self, symbol: str, interval: int, change_threshold: int, stop_loss: float, 
        spend_percent: int, counter_threshold: int, profit_margin: float) -> None:
        self.symbol = symbol                                    # symbol of the asset
        self.interval = interval                                # interval of time to consider price changes
        self.change_threshold = change_threshold                # threshold of price change to consider increasing `self.counter`
        self.counter_threshold = counter_threshold              # threshold of `self.counter` to execute a trade
        self.stop_loss = stop_loss                              # stop loss percentage
        self.spend_percent = spend_percent                      # percentage of spendable amount to use for the trade
        self.profit_margin = profit_margin                      # profit margin percentage
        self.rules = {
            "min_price": 0.001,
            "min_qty": 0.1, 
            "step_size": 0.1,
        }                                                       # rules for the asset (min lot size, etc)
        self.price = 0.0                                        # current price of the asset
        self.change = 0.0                                       # current change in price of the asset
        self.counter = 0                                        # current number of times the price change has surpassed `self.change_threshold`
        self.trading = False                                    # whether or not the asset is currently trading
   
    def _update_values(self) -> bool:
        """
        Updates the asset's price and change.
        """
        present = get_data(self.symbol)
        past =  get_data(self.symbol, self.interval)
        self.change = round(((present.last_price - past.last_price)/present.last_price) * 100, 2)
        self.price = present.last_price

    def _is_profitable(self) -> bool:
        return self.counter > self.counter_threshold

    def run(self) -> None:
        """
        The main function. It updates the price, detects rising prices and executes trades.
        """
        # we don't want to trade if we're already trading
        if self.trading or self.price is None:
            return
        self._update_values()
        if self._is_profitable():
            thread = threading.Thread(target=self._execute_trade)
            thread.start()
            self.counter = 0
        elif self.change > self.change_threshold:
            self.counter += 1
        else:
            self.counter = 0
    
    def _execute_trade(self) -> None:
        # This sucks, the code is basically a prototype and could be optimized and refactored to be more readable
        # and handle errors.
        try:
            print(f"trying... {self.symbol}")
            buy_quantity = self._get_buy_quantity()
        except Exception as e:
            print(e)
            return
        initial_capital = self._get_spendable()
        self.trading = True
        print(f"Buying... {self.symbol}")
        try:
            buy_order = Order(
                symbol=self.symbol, 
                side="BUY", 
                type="LIMIT", 
                quantity=buy_quantity,
                price=self.price
            )
        except Exception as e:
            print(e)
            return
        print(f"New buy order created for {buy_order.quantity} of {buy_order.symbol} at ${buy_order.price}")
        while not buy_order.was_fullfiled():
            continue
        print(f"Buy order fulfilled at {buy_order.symbol}, {buy_order.quantity}, {buy_order.price}")
        sell_quantity = self._get_sell_quantity()
        try:     
            sell_order = Order(
                symbol=self.symbol, 
                side="SELL", 
                type="LIMIT", 
                quantity=sell_quantity,
                price=round(self.price * self.profit_margin, 4)
            )
        except Exception as e:
            print(e)
            return
        while not sell_order.was_fullfiled():
            self._update_values()
            if self._reached_max_loss(buy_order):
                sell_order = Order(
                    symbol=self.symbol, 
                    side="SELL", 
                    type="MARKET", 
                    quantity=sell_quantity
                )
        print(f"Sold {self.symbol}")
        self.trading = False
        final_capital = self._get_spendable()
        profit_loss = final_capital - initial_capital
        print(f"Profit/Loss of ${profit_loss:.4f}")

    def _get_buy_quantity(self) -> float:
        self._update_values()
        spendable = self._get_spendable()
        capital = spendable * self.spend_percent
        assert capital > self.rules["min_price"], "insufficient capital | min_price"
        quantity = capital / self.price
        assert quantity > self.rules["min_qty"], "insufficient capital | min_qty"
        quantity = self._format(quantity)
        return quantity
    
    def _get_sell_quantity(self):
        total_quantity = float(PrivateAPI.get_balance(self.symbol.replace("USDT", "")))
        sell_quantity = self._format(total_quantity)
        return sell_quantity

    def _format(self, balance: float) -> float:
        """
        Formats a given quantity to fit Binance's constraints
        """
        decimals = int(str(self.rules["step_size"]).split(".")[1]) # number of decimals in the step size
        quantity = math.floor(balance * (10 ** decimals) / (10 ** decimals)) # fit the quantity to the step size
        return quantity
    
    def _reached_max_loss(self, order: Order) -> bool:
        return self.price <= order.price * self.stop_loss
    
    def _get_spendable(self) -> float:
        return float(PrivateAPI.get_balance("USDT"))
    
        
