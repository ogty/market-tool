import schedule
import time
import datetime

from component.download_update import download_update
from totalling import totalling
from market_trend import (
    generate_schedule, 
    is_open,
    trend
)


def market_close():
    trend()
    totalling()

# Create schedule
waste_schedule = ["11:40", "11:50", "12:00", "12:10", "12:20"]
time_schedule = generate_schedule(range(9, 15), waste_schedule)

while True:
    if is_open():
        [schedule.every().day.at(i).do(trend) for i in time_schedule]
        schedule.every().day.at("15:00").do(market_close)

        while True:
            if not is_open():
                break

            schedule.run_pending()
            time.sleep(1)
    else:
        time.sleep(1)