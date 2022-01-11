import time
import datetime
import sys

import schedule

from src import (
    schedule_generator as sg,
    loading,
    market_trend as mt,
    totalling
)


time_schedule = sg.ScheduleGenerator(range(9, 15), step=5).delete(start="11:35", end="12:30")

oldest_day = datetime.datetime.now().day
latest_day = 0

loading = loading.loading_spinner()
while True:
    if mt.is_open():
        today = datetime.datetime.now().strftime("%Y/%m/%d")
        print(f"\n\n{today}")

        [schedule.every().day.at(i).do(mt.trend) for i in time_schedule]
        schedule.every().day.at("15:05").do(totalling.totalling)
        schedule.every().day.at("15:06").do(mt.category_totalling)

        while True:
            schedule.run_pending()
            time.sleep(1)
            
            latest_day = datetime.datetime.now().day
            if latest_day != oldest_day:
                break
        
        oldest_day = latest_day
    else:
        print("Holiday  ", end="\b")
        while True:
            if mt.is_open():
                break

            sys.stdout.write(next(loading))
            sys.stdout.flush()
            time.sleep(0.5)
            sys.stdout.write("\b")
