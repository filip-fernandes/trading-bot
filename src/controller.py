from asset import Asset
from api import PrivateAPI, PublicAPI
import time

class Controller:

    def __init__(self, threshold: float, interval: int, primary: str) -> None:
        self.assets = [Asset(symbol, interval, threshold) for symbol in PublicAPI().get_all_symbols(primary)] 
        self.primary = primary
 
    def run(self):
        # initialize how much the assets can spend
        for i in range(1):
            spend = float(PrivateAPI().get_balance(self.primary)["content"][0])
            print(spend, type(spend))
            for asset in self.assets:
                asset.spendable = spend
                asset.run()

    def balance(self):
        pass

def main():
    con = Controller(0.1, 5.0, "USDT")
    con.run() 

main()