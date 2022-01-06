import json
import os
import time

from dotenv import load_dotenv
from selenium import webdriver

from settings import DATA_DIR

load_dotenv()


x_path = open(os.path.join(DATA_DIR, "x_path.json"), "r", encoding="utf-8")
config = json.load(x_path)


class Trade:
    def __init__(self, code: str, shares: str, price: str) -> None:
        username = os.getlogin()
        absolute_directory_path = os.getcwd()

        options = webdriver.ChromeOptions()

        # Setting option
        options.add_argument(f"--user-data-dir=C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data")
        options.add_argument("--profile-directory=Profile 4")
        driver = webdriver.Chrome(executable_path=f"{absolute_directory_path}\\chromedriver.exe", chrome_options=options)

        self.driver = driver
        self.code = code
        self.shares = shares
        self.price = price
    
    def click_path(self, xpath: str) -> None:
        element = self.driver.find_element_by_xpath(xpath)
        element.click()
        time.sleep(1)

    def send_data(self, xpath: str, data: str) -> None:
        element = self.driver.find_element_by_xpath(xpath)
        element.send_keys(data)
        time.sleep(1)

    # default:s buy(whitch=1)
    def main(self, which=1) -> None:
        self.driver.get(config["URL"])
        self.click_path(config["LOGIN"])
        self.click_path(config["TRANSACTION"])
        self.click_path(config["SELECT_MARKET"])

        if which:
            self.click_path(config["BUY"])
        else:
            self.click_path(config["SELL"])

        self.send_data(config["COMPANY_CODE"], self.code)
        self.send_data(config["NUM_OF_SHARES"], self.shares)
        self.send_data(config["PRICE"], self.price)

        self.click_path(config["ABBREVIATIONS"])
        self.click_path(config["SUBMIT"])

    def buy(self) -> None:
        self.main()
        self.driver.close()

    def sell(self) -> None:
        self.main(which=0)
        self.driver.close()

que = {}
while True:
    print(que.keys())

    code = input("\nCode: ")
    shares = input("Shares: ")
    price = input("Purchase price: ")

    try:
        if que[code]:
            que[code].sell()
            del que[code]
    except KeyError:
        que[code] = Trade(code, shares, price)
        que[code].buy()
    except KeyboardInterrupt:
        break
