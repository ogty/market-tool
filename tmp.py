import pandas as pd
import datetime

from component.dataframe_slicer import df_slicer
from component.market_data_acquisition import MarketDataAcquisition


MarketDataAcquisition().save()

month = datetime.datetime.now().month
day = datetime.datetime.now().day

up_path = f"./market_data/{month}/{day}_up.csv"
down_path = f"./market_data/{month}/{day}_down.csv"

df_up = pd.read_csv(up_path)
df_down = pd.read_csv(down_path)

up_splited = df_slicer(df_up, 100)
down_splited = df_slicer(df_down, 100)
