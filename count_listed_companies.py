import pandas as pd


df = pd.read_csv("./data/data_j.csv")
result = [i for i in df["コード"].to_list() if len(str(i)) == 4]

print(len(result))