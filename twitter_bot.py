import os
from dotenv import load_dotenv
import tweepy
import schedule
import time
import requests
import datetime
from bs4 import BeautifulSoup

from market_trend import generate_schedule

load_dotenv()


client = tweepy.Client(
    os.environ["BEARER_TOKEN"], 
    os.environ["API_KEY"], 
    os.environ["API_KEY_SECRET"], 
    os.environ["ACCESS_TOKEN"], 
    os.environ["ACCESS_TOKEN_SECRET"]
)

# TODO: Run "count_listed_companies.py" periodically -> update ALL_COMPANIES
def trend() -> None:
    ALL_COMPANIES = 4136

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

    print(message)
    client.create_tweet(text=message)

# Create schedule
waste_schedule = ["11:40", "11:50", "12:00", "12:10", "12:20"]
time_schedule = generate_schedule(range(9, 15), waste_schedule)
time_schedule.append("15:00")
[schedule.every().day.at(i).do(trend) for i in time_schedule]

while True:
    schedule.run_pending()
    time.sleep(1)
