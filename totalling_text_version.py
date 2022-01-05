import pandas as pd
import datetime
import statistics
import os
import matplotlib.pyplot as plt
import japanize_matplotlib

from component.dataframe_slicer import df_slicer
from component.market_data_acquisition import MarketDataAcquisition


def totalling() -> None:
    # Some Variables
    columns = ["Range", "Market", "Rate", "Price", "Volume"]
    oldest_text = ""
    today = datetime.datetime.now().strftime("%Y/%m/%d")
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day

    # Data Download and Save CSV
    MarketDataAcquisition().save()

    # Read template text and replace "today" to "today"
    with open("./data/totalling_template.txt", "r", encoding="utf-8") as f:
        template = f.read()
    result_text = template.replace("today", today)

    # If the folder does not exist, create it.
    save_path = f"./totalling_data/{month}"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Read CSV and DataFrame slice
    df_up = pd.read_csv(f"./market_data/{month}/{day}_up.csv")
    df_down = pd.read_csv(f"./market_data/{month}/{day}_down.csv")
    up_splited = df_slicer(df_up, 100)
    down_splited = df_slicer(df_down, 100)

    # Main Process
    up_down = {"up": up_splited, "down": down_splited}
    for title, splited in up_down.items():
        oldest = [""]
        graph_data = []
        tmp_result = ""

        for i in range(len(splited)):
            # Range
            start = str(i * 100 + 1).rjust(4)
            end = str((i + 1) * 100).rjust(4)

            # Rate, Volume, Price
            common_line_data = ""
            for column, space in zip(["rate", "price", "volumes"], range(6, 9)):
                tmp_data = splited[i][column].to_list()
                tmp_median = round(statistics.median(tmp_data), 2)
                common_line_data += f" | {str(tmp_median).rjust(space)}"

            # Market
            market_data = dict(splited[i]["market"].value_counts())
            num_of_market = sum([v for v in market_data.values()])
            most_num_market = next(iter(market_data))
            rate_market = round((market_data[most_num_market] / num_of_market) * 100)
            rate_market = str(rate_market).rjust(3)

            # Update the value, and if it is the same market as before, use the ellipsis
            oldest_text = most_num_market
            if oldest[-1] == most_num_market:
                most_num_market = "  〃   "
            oldest.append(oldest_text)

            # Create the final string
            market_line_data = f"{most_num_market}({rate_market}%)"
            tmp_result += f"{start} ~ {end}{common_line_data} | {market_line_data}\n"
            common_data = common_line_data.split(" | ")

            graph_data.append([
                f"{start}〜{end}", 
                market_line_data, 
                common_data[1], 
                common_data[2], 
                common_data[3]
            ])

        # Creat and Save Graphs
        df = pd.DataFrame(graph_data, columns=columns)

        fig = plt.figure()
        plt.axis("off")
        plt.axis("tight")
        plt.table(
            cellText=df.values,
            colLabels=df.columns,
            loc="center",
            bbox=[0, 0, 1, 1]
        )

        plt.title(f"{title} Totalling {today}")
        fig.savefig(f"{save_path}/{day}_{title}.png")

        # Update "result_text"
        result_text = result_text.replace("$$$", tmp_result, 1)

    # Display and Save 
    print(result_text)
    with open(f"{save_path}/{day}.txt", "w", encoding="utf-8") as f:
        f.write(result_text)

if __name__ == "__main__":
    totalling()