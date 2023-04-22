from asset import Asset
from api import PrivateAPI, PublicAPI
import time

class Controller:

    def __init__(self, interval: int, change_threshold: float, primary: str, profit_margin: float, 
        spend_percent: int, counter_threshold: int, stop_loss: float) -> None:
        symbols = PublicAPI.get_all_symbols(primary)
        self.assets = [Asset(
            symbol, 
            interval, 
            change_threshold, 
            stop_loss, 
            spend_percent,
            counter_threshold,
            profit_margin,
        ) for symbol in symbols if symbol != "BTTCUSDT"] # this coin is weird 

    def run(self):
        for asset in self.assets:
            asset.run()
    
    def balance(self):
        pass
