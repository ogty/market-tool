import schedule
import time


def greet(name):
    print(f"Hi, {name}")

name = "ogata"
schedule.every().day.at("15:24").do(greet, name=name)

while True:
    schedule.run_pending()
    time.sleep(1)