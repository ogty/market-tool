from bs4 import BeautifulSoup
import datetime
import os
import pandas as pd
import requests
from tqdm import tqdm


class MarketDataAcquisition:
    def __init__(self, category=1) -> None:
        self.category = category

    def category_max_page_num(self) -> int:
        url = f"https://info.finance.yahoo.co.jp/ranking/?kd={self.category}&tm=d&vl=a&mk=1&p=1"
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        tag = soup.select("[class='ymuiPagingBottom clearFix']")
        result = int(tag[0].text.split("...")[1].rstrip("次へ"))
        
        return result

    def ranking_data(self) -> list:
        codes = []
        markets = []
        prices = []
        rates = []
        volumes = []

        result = []

        max_page_num = self.category_max_page_num() + 1
        for i in tqdm(range(max_page_num)):
            if not i == 0:
                url = f"https://info.finance.yahoo.co.jp/ranking/?kd={self.category}&tm=d&vl=a&mk=1&p={i}"
                html = requests.get(url)
                soup = BeautifulSoup(html.content, "html.parser")

                code = soup.select("[class='txtcenter']")
                codes += [code[i].text for i in range(len(code)) if not i % 2 == 0]

                market = soup.select("[class='txtcenter yjSt']")
                markets += [market[i].text for i in range(len(market)) if i % 2 == 0]

                price = soup.select("[class='txtright bold']")
                prices += [float(i.text.replace(",", "")) for i in price]

                rate = soup.select("[class='txtright bgyellow02']")
                rates += [float(i.text.rstrip("%")) for i in rate]

                volume = soup.select("[class='txtright']")
                volumes += [int(i.text.replace(",", "")) for i in volume]

        if self.category == 2:
            codes.reverse()
            markets.reverse()
            prices.reverse()
            rates.reverse()
            volumes.reverse()

        for i in range(len(codes)):
            result.append([codes[i], markets[i], prices[i], rates[i], volumes[i]])

        return result

up = MarketDataAcquisition()
down = MarketDataAcquisition(category=2)

up_result = up.ranking_data()
down_result = down.ranking_data()

columns = ["code", "market", "price", "rate", "volumes"]
result = up_result + down_result
df = pd.DataFrame(result, columns=columns)

month = datetime.datetime.now().month
day = datetime.datetime.now().day

month_path = f"./market_data/{month}"

if not os.path.exists(month_path):
    os.mkdir(month_path)

df.to_csv(f"{month_path}/{day}.csv", index=False)
