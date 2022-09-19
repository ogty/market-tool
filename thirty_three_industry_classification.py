import japanize_matplotlib
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("./data/data_j.csv")
thirty_three_industry_classification = set(list(df["33業種区分"].values))

count = []
for industry in thirty_three_industry_classification:
    industry_df = df[df["33業種区分"] == industry]
    count.append(len(industry_df))

count, thirty_three_industry_classification = zip(
    *sorted(zip(count, thirty_three_industry_classification),
    reverse=True)
)

figure = plt.figure(figsize=(9, 7))
plt.title("33業種区分")
plt.bar(thirty_three_industry_classification, count, color="#344966")
plt.xticks(rotation=90)
plt.ylabel("企業数")
plt.yticks(range(0, max(count), 50))
plt.subplots_adjust(bottom=0.25)
figure.savefig("./images/thirty_three_industry_classification.png")
