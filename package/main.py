import urllib
import requests
import pandas as pd
import os
from dotenv import load_dotenv
import tweepy
import schedule
import time
import datetime
from bs4 import BeautifulSoup
import json
import logging

load_dotenv()


client = tweepy.Client(
    os.environ["BEARER_TOKEN"], 
    os.environ["API_KEY"], 
    os.environ["API_KEY_SECRET"], 
    os.environ["ACCESS_TOKEN"], 
    os.environ["ACCESS_TOKEN_SECRET"]
)

ALL_COMPANIES = 0

# download new data file and update constant variable
def download_update() -> None:
    global ALL_COMPANIES

    url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    save_path = "./data/data_j.xls"
    urllib.request.urlretrieve(url, save_path)

    df = pd.read_excel(save_path)
    df.to_csv("./data/data_j.csv", index=False)

    df = pd.read_csv("./data/data_j.csv")
    codes = [i for i in df["コード"].to_list() if len(str(i)) == 4]

    ALL_COMPANIES = len(codes)

def update_logger():
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day

    path = f"./log/{month}"
    if not os.path.exists(path):
        os.makedirs(path)

    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(f"{path}/{day}.log")
    logging.basicConfig(
        format="%(asctime)s | %(message)s", 
        level=logging.INFO,
        handlers=[stream_handler, file_handler]
    )
    logger = logging.getLogger(__name__)

def trend() -> None:
    url = "https://info.finance.yahoo.co.jp/ranking/?kd=1&tm=d&mk=1"
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    data = soup.select("[class='rankdataPageing yjS']")
    result = data[0].text
    up_companies = result.split("/")[1].replace("件中", "")
    
    up_rate = round(int(up_companies) / ALL_COMPANIES, 3)
    down_rate = round(1.0 - up_rate, 3)

    now = datetime.datetime.now()
    message = f"{now}\nUP：{up_rate * 100}%\nDOWN：{down_rate * 100}%"
    log_message = f"UP:{up_rate * 100}% | DOWN：{down_rate * 100}%"

    logger.info(log_message)
    print(message)

    # Twitter bot
    client.create_tweet(text=message)

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

# Get an annual leave schedule
def market_holidays(path: str) -> None:
    url = "https://www.jpx.co.jp/corporate/about-jpx/calendar/index.html"
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    data = soup.select("[class='a-center']")
    holidays = [data[i].text for i in range(len(data)) if i % 2 == 0]

    holidays = list(filter(lambda x: x.startswith(year), holidays))
    holidays = list(map(lambda x: x[:-3], holidays))

    with open(path, "w", encoding="utf-8") as f:
        for holiday in holidays:
            f.write(f"{holiday}\n")

# Working day or Holiday?
def is_open() -> bool:
    year = str(datetime.datetime.now().year)
    
    path = f"./data/{year}.txt"
    if not os.path.exists(path):
        market_holidays(path)
    
    with open(path, "r", encoding="utf-8") as f:
        holidays = [holiday.rstrip() for holiday in f]

    weekday = datetime.datetime.now().weekday()
    now = datetime.datetime.now().strftime("%Y/%m/%d")

    if weekday < 5:
        if not now in holidays:
            return True
        else:
            return False
    else:
        return False

# Create schedule
waste_schedule = ["11:40", "11:50", "12:00", "12:10", "12:20"]
time_schedule = generate_schedule(range(9, 15), waste_schedule)
time_schedule.append("15:00")

oldest_month = 0
while True:
    latest_month = datetime.datetime.now().month

    # Initialize and Update "./data/data_j.csv"
    if latest_month != oldest_month:
        download_update()
        oldest_month = latest_month

    if is_open():
        [schedule.every().day.at(i).do(trend) for i in time_schedule]

        while True:
            if not is_open():
                break

            schedule.run_pending()
            time.sleep(1)
    else:
        time.sleep(1)