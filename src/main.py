from controller import Controller


def main() -> None:

    INTERVAL = 70
    CHANGE_THRESHOLD = 2.3
    PRIMARY = "USDT"
    PROFIT_MARGIN = 1.051
    SPEND_PERCENT = 0.5
    COUNTER_THRESOLD = 6
    STOP_LOSS = 0.977

    controller = Controller(
        interval=INTERVAL,
        change_threshold=CHANGE_THRESHOLD,
        primary=PRIMARY,
        profit_margin=PROFIT_MARGIN,
        spend_percent=SPEND_PERCENT,
        counter_threshold=COUNTER_THRESOLD,
        stop_loss=STOP_LOSS
    )

    while True:
        controller.run()


if __name__ == "__main__":
    main()
