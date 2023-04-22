from feed import feed, curr_time
from controller import Controller
import time
import os


def main():
    RATE = 1

    INTERVAL = 20
    CHANGE_THRESHOLD = 2.88
    PRIMARY = "USDT"
    PROFIT_MARGIN = 1.051
    SPEND_PERCENT = 0.5
    COUNTER_THRESOLD = 2
    STOP_LOSS = 0.98

    controller = Controller(
        interval=INTERVAL,
        change_threshold=CHANGE_THRESHOLD,
        primary=PRIMARY,
        profit_margin=PROFIT_MARGIN,
        spend_percent=SPEND_PERCENT,
        counter_threshold=COUNTER_THRESOLD,
        stop_loss=STOP_LOSS
    )
    
    # Feed the db with the initial data
    
    for i in range(INTERVAL):
        feed(PRIMARY)
        time.sleep(RATE)
    
    print("Database fed. Initializing controller...")

    while True:
        feed(PRIMARY)
        controller.run()
        time.sleep(RATE)

if __name__ == "__main__":
    main()
