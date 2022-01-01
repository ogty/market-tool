import urllib
import requests
import pandas as pd


url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
save_path = "./data/data_j.xls"
urllib.request.urlretrieve(url, save_path)

df = pd.read_excel(save_path)
df.to_csv("./data/data_j.csv", index=False)