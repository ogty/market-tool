import schedule
import time
import datetime
import sys

from component.loading import loading_spinner
from component.generate_schedule import generate_schedule
from totalling_text_version import totalling
from market_trend import is_open, trend


# Create schedule
waste_schedule = ["11:40", "11:50", "12:00", "12:10", "12:20"]
time_schedule = generate_schedule(range(9, 15), step=10, waste_schedule=waste_schedule)

loading = loading_spinner()

while True:
    if is_open():
        today = datetime.datetime.now().strftime("%Y/%m/%d")
        print(f"\n\n{today}")

        [schedule.every().day.at(i).do(trend) for i in time_schedule]
        schedule.every().day.at("15:05").do(totalling)

        while True:
            if not is_open():
                break

            schedule.run_pending()
            time.sleep(1)
    else:
        print("Holiday  ", end="\b")
        while True:
            if is_open():
                break

            sys.stdout.write(next(loading))
            sys.stdout.flush()
            time.sleep(0.5)
            sys.stdout.write("\b")