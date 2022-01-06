import datetime
import os
import sys
import time

from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import pandas as pd
import schedule

sys.path.append("../")
from component.generate_schedule import generate_schedule


# TODO: Too much use of int
class JudgeShortSaleCode:
    def __init__(self, category_number: int, download=True, path="") -> None:
        self.category_number = category_number
        self.df = pd.DataFrame()
        self.data_j = pd.read_csv("../data/data_j.csv")
        self.columns = ["銘柄名", "市場・商品区分", "33業種区分"]

        if download:
            self.acquisition()
        else:
            self.df = pd.read_csv(path)

    def info(self, code: int) -> list:
        result = [code]
        selected_df = self.data_j[self.data_j["コード"] == code]

        for i in range(len(self.columns)):
            result += selected_df[self.columns[i]].tolist()

        return result

    def category_max_page_num(self) -> int:
        url = f"https://info.finance.yahoo.co.jp/ranking/?kd={self.category_number}&tm=d&vl=a&mk=1&p=1"
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        tag = soup.select("[class='ymuiPagingBottom clearFix']")
        result = int(tag[0].text.split("...")[1].rstrip("次へ"))
        
        return result

    def acquisition(self) -> pd.DataFrame:
        columns = ["code", "price", "rate"]
        codes = []
        prices = []
        rates = []

        max_page_num = self.category_max_page_num()
        bar = tqdm(total=max_page_num)

        for i in range(1, max_page_num + 1):
            url = f"https://info.finance.yahoo.co.jp/ranking/?kd={self.category_number}&tm=d&vl=a&mk=1&p={i}"
            html = requests.get(url)
            soup = BeautifulSoup(html.content, "html.parser")

            code = soup.select("[class='txtcenter']")
            codes += [code[i].text for i in range(len(code)) if not i % 2 == 0]

            price = soup.select("[class='txtright bold']")
            prices += [float(i.text.replace(",", "")) for i in price]

            rate = soup.select("[class='txtright bgyellow02']")
            rates += [float(i.text.rstrip("%")) for i in rate]

            bar.update(1)

        tmp = []
        for i in range(len(codes)):
            tmp.append([codes[i], prices[i], rates[i]])

        df = pd.DataFrame(tmp, columns=columns)

        self.df = df

    def select(self, codes: list, price: float, rate: float, campany_info=False) -> list or pd.DataFrame:
        if self.category_number == 1:
            selected_df = self.df[(self.df["rate"] >= rate) & (self.df["price"] >= price)]
        else:
            selected_df = self.df[(self.df["rate"] <= rate) & (self.df["price"] >= price)]

        selected_codes = selected_df["code"].tolist()
        result = list(map(lambda x: int(x) if int(x) in codes else None, selected_codes))

        for _ in range(result.count(None)):
            result.remove(None)

        if campany_info:
            tmp = []
            for code in result:
                tmp_result = self.info(code)

                if len(tmp_result) == 4:
                    tmp.append(tmp_result)
            
            columns = ["コード"] + self.columns

            return pd.DataFrame(tmp, columns=columns)
        else:
            return result

def matched() -> None:
    os.system("cls")
    up = JudgeShortSaleCode(1).select(short_sale_codes, 5000, 3)
    now = datetime.datetime.now()
    print(now)
    print(up)

with open("../data/short_sale_codes.txt", "r", encoding="utf-8") as f:
    short_sale_codes = [int(code.rstrip()) for code in f]

waste_schedule = ["11:30", "12:00"]
time_schedule = generate_schedule(range(9, 15), step=30, waste_schedule=waste_schedule)
[schedule.every().day.at(i).do(matched) for i in time_schedule]

while True:
    schedule.run_pending()
    time.sleep(1)