from bs4 import BeautifulSoup
import datetime
from dotenv import load_dotenv
import json
import os
import pandas as pd
import requests
import schedule
import sys
import time
import tweepy
import urllib


load_dotenv()
oldest_month = 0
ALL_COMPANIES = 0

client = tweepy.Client(
    os.environ["BEARER_TOKEN"], 
    os.environ["API_KEY"], 
    os.environ["API_KEY_SECRET"], 
    os.environ["ACCESS_TOKEN"], 
    os.environ["ACCESS_TOKEN_SECRET"]
)

def loading_spinner():
    while True:
        for cursor in "|/-\\":
            yield cursor

# download latest data file and update constant variable
def download_update() -> int:
    url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    save_path = "./data/data_j.xls"
    urllib.request.urlretrieve(url, save_path)

    df = pd.read_excel(save_path)
    df.to_csv("./data/data_j.csv", index=False)

    df = pd.read_csv("./data/data_j.csv")
    codes = [i for i in df["コード"].to_list() if len(str(i)) == 4]
    result = len(codes)

    return result

def trend() -> None:
    global ALL_COMPANIES
    global oldest_month 

    latest_month = datetime.datetime.now().month

    if latest_month != oldest_month:
        ALL_COMPANIES = download_update()
        oldest_month = latest_month

    url = "https://info.finance.yahoo.co.jp/ranking/?kd=1&tm=d&mk=1"
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    data = soup.select("[class='rankdataPageing yjS']")
    result = data[0].text
    up_companies = result.split("/")[1].replace("件中", "")
    
    up_rate = round((int(up_companies) / ALL_COMPANIES) * 100, 3)
    down_rate = round((1.0 - up_rate) * 100, 3)

    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    message = f"{now} | UP: {up_rate} | DOWN: {down_rate}"
    twitter_message = f"{now}\nUP：{up_rate}\nDOWN：{down_rate}"

    # Twitter bot
    client.create_tweet(text=twitter_message)

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

def generate_schedule(hour_list, step=30, include=True, waste_schedule=[]) -> list:
    time_schedule = []

    for hour in hour_list:
        for minute in range(0, 51, step):
            if len(str(hour)) == 1:
                hour = f"0{hour}"
            if len(str(minute)) == 1:
                minute = f"0{minute}"

            time_schedule.append(f"{hour}:{minute}")

    if include:
        if hour_list[-1] == 23:
            pass
        else:
            time_schedule.append(f"{hour_list[-1] + 1}:00")
        
    for waste in waste_schedule:
        time_schedule.remove(waste)

    return time_schedule

# Get an annual leave schedule
def market_holidays(year: str, path: str) -> None:
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
        market_holidays(year, path)
    
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
time_schedule = generate_schedule(range(9, 15), step=10, waste_schedule=waste_schedule)

loading = loading_spinner()
while True:
    if is_open():
        today = datetime.datetime.now().strftime("%Y/%m/%d")
        print(f"\n\n{today}")

        [schedule.every().day.at(i).do(trend) for i in time_schedule]

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