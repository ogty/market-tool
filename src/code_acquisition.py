import re

from bs4 import BeautifulSoup
import requests


RE_MAX_PAGE_NUM = re.compile(r"1〜50/(?P<max_page_num>[\d]+)件")
RE_CODE = re.compile(r".+(\d{4}).+掲示板")


class CodeAcquisition:
    
    def __init__(self, category_type: str) -> None:
        self.category_type = category_type
        self.codes = []
        self.base_url = "https://finance.yahoo.co.jp/stocks/ranking/"

    def max_page_scraping(self) -> int:
        url = self.base_url + self.category_type
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        data = soup.select('p')

        for i in data:
            match = RE_MAX_PAGE_NUM.search(i.text)
            if not match:
                continue

            return int(match.group("max_page_num"))

    def code_scraping(self) -> None:
        for i in range(1, self.max_page_scraping() + 1):
            url = self.base_url + self.category_type + f"?market=all&term=daily&page={i}"
            html = requests.get(url)
            soup = BeautifulSoup(html.content, "html.parser")
            data = soup.select("td")

            for i in data:
                match = re.match(RE_CODE, i.text)
                if not match:
                    continue
                self.codes.append(int(match.group(1)))


if __name__ == "__main__":
    instance = CodeAcquisition("up")
    max_page_number = instance.max_page_scraping()
    instance.code_scraping()
    print(instance.codes)
