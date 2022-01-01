from bs4 import BeautifulSoup
import datetime
from dotenv import load_dotenv
import json
import logging
import os
import requests
import schedule
import time

load_dotenv()


def update_logger():
    today = datetime.datetime.now().strftime("%Y_%m_%d")

    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(f"./log/{today}.log")
    logging.basicConfig(
        format="%(asctime)s | %(message)s", 
        level=logging.INFO,
        handlers=[stream_handler, file_handler]
    )
    logger = logging.getLogger(__name__)

# Logging and send market trend
def trend() -> None:
    ALL_COMAPNIES = 4136

    url = "https://info.finance.yahoo.co.jp/ranking/?kd=1&tm=d&mk=1"
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    data = soup.select("[class='rankdataPageing yjS']")
    result = data[0].text
    up_companies = result.split("/")[1].replace("件中", "")
    
    up_rate = round(int(up_companies) / ALL_COMAPNIES, 3)
    down_rate = 1.0 - up_rate

    message = f"UP: {up_rate} | DOWN: {down_rate}"

    logger.info(message)

    # Slack bot
    requests.post(
        os.environ["WEB_HOOK_URL"], 
        data=json.dumps({
            "text" : message,
            "icon_emoji" : ":dog:",
            "username" : "Trend"
            }
        )
    )

def generate_schedule(hour_list, waste_schedule=[]) -> list:
    time_schedule = []

    for hour in hour_list:
        for minute in range(0, 51, 10):
            if len(str(hour)) == 1:
                hour = f"0{hour}"
            if len(str(minute)) == 1:
                minute = f"0{minute}"

            time_schedule.append(f"{hour}:{minute}")

    for waste in waste_schedule:
        time_schedule.remove(waste)

    return time_schedule

def market_holidays() -> list:
    url = "https://www.jpx.co.jp/corporate/about-jpx/calendar/index.html"
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    data = soup.select("[class='a-center']")
    result = [data[i].text for i in range(len(data)) if i % 2 == 0]

    return result

def is_open() -> bool:
    year = str(datetime.datetime.now().year)
    
    path = f"./data/{year}.txt"
    if not os.path.exists(path):
        data = market_holidays()
        holidays = list(filter(lambda x: x.startswith(year), data))
        holidays = list(map(lambda x: x[:-3], holidays))

        with open(path, "w", encoding="utf-8") as f:
            for holiday in holidays:
                f.write(f"{holiday}\n")
    
    with open(path, "r", encoding="utf-8") as f:
        holidays = f.readlines()

    weekday = datetime.datetime.now().weekday()
    now = datetime.datetime.now().strftime("%Y/%m/%d")

    if weekday < 5:
        if now in holidays:
            return True
    else:
        return False

if __name__ == "__main__":
    # Create schedule
    waste_schedule = ["11:40", "11:50", "12:00", "12:10", "12:20"]
    time_schedule = generate_schedule(range(9, 15), waste_schedule)
    time_schedule.append("15:00")
    
    while True:
        if is_open():
            update_logger()

            # Set schedule
            [schedule.every().day.at(i).do(trend) for i in time_schedule]

            while True:
                if not is_open():
                    break

                schedule.run_pending()
                time.sleep(1)
        else:
            time.sleep(1)