import datetime
import os
from typing import List 

from bs4 import BeautifulSoup
import pandas as pd
import requests
from tqdm import tqdm

import settings


class MarketDataAcquisition:

    def category_max_page_num(self, category_number: int) -> int:
        url = f"https://info.finance.yahoo.co.jp/ranking/?kd={category_number}&tm=d&vl=a&mk=1&p=1"
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        data = soup.select("[class='ymuiPagingBottom clearFix']")
        match = settings.RE_MAX_PAGE_NUM.search(data[0].text)
        result = int(match.group("max_page_num"))

        return result

    def ranking_data(self, category_number: int) -> List[str, str, str, float, float, int]:
        include_new_market_df = pd.read_csv(os.path.join(settings.DATA_DIR, "JP.csv"))

        codes = []
        markets = []
        new_markets = []
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

        for code in codes:
            try:
                new_markets.append(include_new_market_df[(include_new_market_df["コード"] == int(code))]["新市場区分"].tolist()[0])
            except:
                new_markets.append("-")

        if category_number == 2:
            codes.reverse()
            markets.reverse()
            new_markets.reverse()
            prices.reverse()
            rates.reverse()
            volumes.reverse()

        for i in range(len(codes)):
            result.append([codes[i], markets[i], new_markets[i], prices[i], rates[i], volumes[i]])

        return result

    def save(self, connect: bool = False) -> None:
        columns = ["code", "market", "new_market", "price", "rate", "volumes"]

        month = str(datetime.datetime.now().month)
        day = datetime.datetime.now().day
        MONTH_PATH = os.path.join(settings.MARKET_DATA_DIR, month)

        if not os.path.exists(MONTH_PATH):
            os.makedirs(MONTH_PATH)
            
        up = self.ranking_data(1)
        down = self.ranking_data(2)
        
        if connect:
            result = up + down
            df = pd.DataFrame(result, columns=columns)
            df.to_csv(os.path.join(MONTH_PATH, f"{day}.csv"), index=False)
        else:
            df_up = pd.DataFrame(up, columns=columns)
            df_down = pd.DataFrame(down, columns=columns)

            df_up.to_csv(os.path.join(MONTH_PATH, f"{day}_up.csv"), index=False)
            df_down.to_csv(os.path.join(MONTH_PATH, f"{day}_down.csv"), index=False)

if __name__ == "__main__":
    MarketDataAcquisition().save()
