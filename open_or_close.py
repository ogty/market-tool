from bs4 import BeautifulSoup
import datetime
import os
import requests


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

if is_open():
    print("Working Day")
else:
    print("Holiday")