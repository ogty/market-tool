import time
import datetime
import sys

import schedule

from src import (
    generate_schedule as gs,
    loading,
    market_trend as mt,
    totalling
)


# Create schedule
waste_schedule = ["11:40", "11:50", "12:00", "12:10", "12:20"]
time_schedule = gs.generate_schedule(range(9, 15), step=10, delete=waste_schedule)

# loading = loading.loading_spinner()

# oldest_day = datetime.datetime.now().day
# latest_day = 0

# while True:
#     if mt.is_open():
#         today = datetime.datetime.now().strftime("%Y/%m/%d")
#         print(f"\n\n{today}")

#         [schedule.every().day.at(i).do(mt.trend) for i in time_schedule]
#         schedule.every().day.at("15:05").do(totalling.totalling)

#         while True:
#             latest_day = datetime.datetime.now().day

#             schedule.run_pending()
#             time.sleep(1)

#             if latest_day != oldest_day:
#                 break
        
#         oldest_day = latest_day
#     else:
#         print("Holiday  ", end="\b")
#         while True:
#             if mt.is_open():
#                 break

#             sys.stdout.write(next(loading))
#             sys.stdout.flush()
#             time.sleep(0.5)
#             sys.stdout.write("\b")

print(time_schedule)
mt.trend()
totalling.totalling()
