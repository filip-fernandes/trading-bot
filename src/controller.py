from asset import Asset
from public_api import get_all_symbols



class Controller:

    def __init__(self, threshold, interval, primary) -> None:
        self.assets = [Asset(symbol, interval, threshold) for symbol in get_all_symbols(primary)]
        self.orders = []
        self.stop_loss = 0.0
 
    
    def run(self):
        while True:
            orders = [asset.run() for asset in self.assets]


    def balance(self):
        pass

def main():
    con = Controller(0.1, 5.0, "USDT")
    con.run() 

main()