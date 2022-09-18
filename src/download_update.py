import os

import urllib.request
import pandas as pd

from settings import DATA_DIR


# download latest data file and update constant variable
def download_update() -> int:
    XLS_SAVE_PATH = os.path.join(DATA_DIR, "data_j.xls")
    CSV_SAVE_PATH = os.path.join(DATA_DIR, "data_j.csv")

    url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    urllib.request.urlretrieve(url, XLS_SAVE_PATH)

    df = pd.read_excel(XLS_SAVE_PATH)
    df.to_csv(CSV_SAVE_PATH, index=False)

    df = pd.read_csv(CSV_SAVE_PATH)
    codes = [i for i in df["コード"].to_list() if len(str(i)) == 4]
    result = len(codes)

    return result
