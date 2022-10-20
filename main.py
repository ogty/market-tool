import time
import datetime
import sys

import schedule

from src import loading, totalling
from src.schedule_generator import ScheduleGenerator
from src.market_trend import trend, is_open, category_totalling


time_schedule = ScheduleGenerator(range(9, 15), step=5).delete(start="11:35", end="12:30")

oldest_day = datetime.datetime.now().day
latest_day = 0

# TODO: reset schedule?
loading = loading.loading_spinner()
while True:
    if is_open():
        today = datetime.datetime.now().strftime("%Y/%m/%d")
        print(f"\n\n{today}")

        [schedule.every().day.at(i).do(trend) for i in time_schedule]
        schedule.every().day.at("15:05").do(totalling.totalling)
        schedule.every().day.at("15:06").do(category_totalling)

        while True:
            schedule.run_pending()
            time.sleep(1)

            latest_day = datetime.datetime.now().day
            if latest_day != oldest_day:
                break

        oldest_day = latest_day
    else:
        print("Holiday  ", end='\b')
        while True:
            if is_open():
                break

            sys.stdout.write(next(loading))
            sys.stdout.flush()
            time.sleep(0.5)
            sys.stdout.write('\b')
