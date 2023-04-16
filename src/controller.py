from asset import Asset
from api import get_all_symbols, get_balance
import time

class Controller:

    def __init__(self, threshold, interval, primary) -> None:
        self.assets = [Asset(symbol, interval, threshold) for symbol in get_all_symbols(primary)] 
 
    def run(self):
        # initialize how much the assets can spend
        for i in range(1):
            spend = get_balance()
            for asset in self.assets:
                asset.spendable = spend
                asset.run()

    def balance(self):
        pass

def main():
    con = Controller(0.1, 5.0, "USDT")
    con.run() 

main()