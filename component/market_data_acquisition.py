from bs4 import BeautifulSoup
import datetime
import os
import pandas as pd
import requests
from tqdm import tqdm


class MarketDataAcquisition:
    def category_max_page_num(self, category_number: int) -> int:
        url = f"https://info.finance.yahoo.co.jp/ranking/?kd={category_number}&tm=d&vl=a&mk=1&p=1"
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        tag = soup.select("[class='ymuiPagingBottom clearFix']")
        result = int(tag[0].text.split("...")[1].rstrip("次へ"))
        
        return result

    def ranking_data(self, category_number: int) -> list:
        codes = []
        markets = []
        prices = []
        rates = []
        volumes = []

        result = []

        max_page_num = self.category_max_page_num(category_number)
        bar = tqdm(total=max_page_num)

        if category_number == 1:
            bar.set_description("Up")
        else:
            bar.set_description("Down")

        for i in range(1, max_page_num + 1):
            url = f"https://info.finance.yahoo.co.jp/ranking/?kd={category_number}&tm=d&vl=a&mk=1&p={i}"
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

            bar.update(1)

        if category_number == 2:
            codes.reverse()
            markets.reverse()
            prices.reverse()
            rates.reverse()
            volumes.reverse()

        for i in range(len(codes)):
            result.append([codes[i], markets[i], prices[i], rates[i], volumes[i]])

        return result

    def save(self, connect=False) -> None:
        columns = ["code", "market", "price", "rate", "volumes"]

        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        month_path = f"./market_data/{month}"

        if not os.path.exists(month_path):
            os.makedirs(month_path)
            
        up = self.ranking_data(1)
        down = self.ranking_data(2)
        
        if connect:
            result = up + down
            df = pd.DataFrame(result, columns=columns)

            df.to_csv(f"{month_path}/{day}.csv", index=False)
        else:
            df_up = pd.DataFrame(up, columns=columns)
            df_down = pd.DataFrame(down, columns=columns)

            df_up.to_csv(f"{month_path}/{day}_up.csv", index=False)
            df_down.to_csv(f"{month_path}/{day}_down.csv", index=False)
