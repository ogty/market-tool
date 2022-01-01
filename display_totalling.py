import pandas as pd
import datetime
import statistics
import os
import matplotlib.pyplot as plt
import japanize_matplotlib

from component.dataframe_slicer import df_slicer
from component.market_data_acquisition import MarketDataAcquisition


# MarketDataAcquisition().save()

month = datetime.datetime.now().month
day = datetime.datetime.now().day

up_path = f"./market_data/{month}/{day}_up.csv"
down_path = f"./market_data/{month}/{day}_down.csv"

save_path = f"./totalling_data/{month}"

if not os.path.exists(save_path):
    os.makedirs(save_path)

df_up = pd.read_csv(up_path)
df_down = pd.read_csv(down_path)

up_splited = df_slicer(df_up, 100)
down_splited = df_slicer(df_down, 100)

range_text = "Range".center(13)
market_text = "Market".center(16)
median_text = "Rate".center(8)
price_text = "Price".center(9)
volume_text = "Volume".center(10)

oldest_list = [""]
oldest_text = ""

columns = ["Range", "Market", "Rate（％）", "Price（円）", "Volume"]

splited_list = [up_splited, down_splited]
for splited_index, splited in enumerate(splited_list):
    print(f"\n{range_text}|{market_text}|{median_text}|{price_text}|{volume_text}")
    print("=" * 60)
    oldest = [""]
    result = []

    for i in range(len(splited)):
        # rate
        rate_data = splited[i]["rate"].to_list()
        rate_median = round(statistics.median(rate_data), 2)
        display_rate = str(rate_median).rjust(6)

        # volume
        volumes_data = splited[i]["volumes"].to_list()
        volumes_median = round(statistics.median(volumes_data), 2)
        display_volumes = str(volumes_median).rjust(8)
        
        # price
        price_data = splited[i]["price"].to_list()
        price_median = round(statistics.median(price_data), 2)
        display_price = str(price_median).rjust(7)

        # market
        market_data = dict(splited[i]["market"].value_counts())
        num_of_market = sum([v for v in market_data.values()])
        most_num_market = next(iter(market_data))

        rate_market = round((market_data[most_num_market] / num_of_market) * 100)
        rate_market = str(rate_market).rjust(3)

        oldest_text = most_num_market

        if oldest[-1] == most_num_market:
            most_num_market = "   〃  "

        display_market = f"{most_num_market}({rate_market}%)"

        # range
        start = str(i * 100 + 1).rjust(4)
        end = str((i + 1) * 100).rjust(4)

        if not most_num_market == "マザーズ":
            print(f" {start} ~ {end} | {display_market}  | {display_rate} | {display_price} | {display_volumes}")
        else:
            print(f" {start} ~ {end} | {display_market} | {display_rate} | {display_price} | {display_volumes}")
        
        oldest.append(oldest_text)

        save_market = f"{most_num_market}：{rate_market}%"

        result.append([f"{start}〜{end}", save_market, rate_median, price_median, volumes_median])

    df = pd.DataFrame(result, columns=columns)

    fig = plt.figure()
    plt.axis("off")
    plt.axis("tight")
    plt.table(
        cellText=df.values,
        colLabels=df.columns,
        loc="center",
        bbox=[0, 0, 1, 1]
    )

    if splited_index == 0:
        # plt.savefig(f"{save_path}/{day}_up.png")
        fig.savefig(f"{save_path}/{day}_up.png")
    else:
        # plt.savefig(f"{save_path}/{day}_down.png")
        fig.savefig(f"{save_path}/{day}_down.png")
