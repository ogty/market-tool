import schedule
import time
import datetime

from component.download_listed_stocks import download
from totalling import totalling
from component.market_trend import (
    update_logger, 
    market_holidays, 
    generate_schedule, 
    is_open,
    trend
)


def market_close() -> None:
    trend()
    totalling()

# Create schedule
waste_schedule = ["11:40", "11:50", "12:00", "12:10", "12:20"]
time_schedule = generate_schedule(range(9, 15), waste_schedule)

oldest_month = 0

while True:
    month = datetime.datetime.now().month

    # Update "./data/data_j.csv"
    if month != oldest_month:
        download()
        oldest_month = month

    if is_open():
        update_logger()

        # Set schedule
        [schedule.every().day.at(i).do(trend) for i in time_schedule]
        schedule.every().day.at("15:00").do(market_close)

        while True:
            if not is_open():
                break

            schedule.run_pending()
            time.sleep(1)
    else:
        time.sleep(1)