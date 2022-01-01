import pandas as pd


df = pd.read_csv("./data/data_j.csv")
result = len([i for i in df["コード"].to_list() if len(str(i)) == 4])

print(result)