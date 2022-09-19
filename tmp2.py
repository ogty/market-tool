import json

from datetime import datetime
import japanize_matplotlib
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("./data/data_j.csv")


def stocks_with_high_hv() -> dict:
    with open("./data/historical_volatility/hv-2022-09-20.json", 'r', encoding="utf-8") as f:
        data = json.load(f)
    
    upper_quartile = data["summaryStatistics"]["75%"]

    ok = []
    for code, hv in data["data"].items():
        if hv >= upper_quartile:
            ok.append(code)

    thirty_three_industry_classification = []
    for code in ok:
        stock_data = df[df["コード"] == int(code)]
        thirty_three_industry_classification.append(stock_data["33業種区分"].values[0])

    columns = set(thirty_three_industry_classification)
    result = {column: thirty_three_industry_classification.count(column) for column in columns}
    return result


def all_listed_stocks() -> dict:
    thirty_three_industry_classification = set(df["33業種区分"].tolist())

    count = []
    for column in thirty_three_industry_classification:
        count.append(len(df[df["33業種区分"] == column]))

    count, thirty_three_industry_classification = zip(
        *sorted(zip(count, thirty_three_industry_classification),
        reverse=True)
    )

    result = {k: v for k, v in zip(thirty_three_industry_classification, count)}
    return result


high_hv_data = stocks_with_high_hv()
all_data = all_listed_stocks()

result = {k: (v / all_data[k] * 100) for k, v in high_hv_data.items()}
result = sorted(result.items(), key=lambda x: x[1], reverse=True)

today = datetime.today().strftime("%Y-%m-%d")
figure = plt.figure(figsize=(9, 7))
plt.title("ヒストリカルボラティリティ(HV)が第三四分位数より大きい銘柄の業種に占める割合")
plt.bar(*zip(*result), color="#344966")
plt.xticks(rotation=90)
plt.ylabel("割合(%)")
plt.yticks(range(0, 100, 5))
plt.subplots_adjust(bottom=0.25)
figure.savefig(f"./images/hv-rate-{today}.png")
