from bs4 import BeautifulSoup
import requests

from settings import RE_MAX_PAGE_NUM


class CodeAcquisition:
    def __init__(self, cateogry_number: int) -> None:
        self.cateogry_number = cateogry_number
        self.codes = []

    def max_page_scraping(self) -> int:
        url = f"https://info.finance.yahoo.co.jp/ranking/?kd={self.cateogry_number}&tm=d&vl=a&mk=1&p=1"
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        data = soup.select("[class='ymuiPagingBottom clearFix']")
        match = RE_MAX_PAGE_NUM.search(data[0].text)
        result = int(match.group("max_page_num"))

        return result

    def code_scraping(self) -> None:
        for i in range(1, self.max_page_scraping() + 1):
            url = f"https://info.finance.yahoo.co.jp/ranking/?kd={self.cateogry_number}&tm=d&vl=a&mk=1&p={i}"
            html = requests.get(url)
            soup = BeautifulSoup(html.content, "html.parser")
            data = soup.select("[class='txtcenter']")
            self.codes += [data[i].text for i in range(len(data)) if not i % 2 == 0]
