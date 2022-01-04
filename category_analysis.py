import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

from component.analizer import Analizer
from component.dataframe_slicer import df_slicer


# analizer = Analizer([])
# print(analizer.distribution("市場第一部（内国株）", "マザーズ（内国株）"))

df_up = pd.read_csv("./market_data/1/4_up.csv")
splited_dfs = df_slicer(df_up, 100)

for i, splited_df in enumerate(splited_dfs[:]):
    start = str(i * 100 + 1).rjust(4)
    end = str((i + 1) * 100).rjust(4)
    
    analizer = Analizer(splited_df["code"])
    result = analizer.category()
    
    print(f"{start} ~ {end}")
    print(result)

    result_keys = [k for k in result.keys()]
    result_values = [v for v in result.values()]

    plt.title(f"{start}〜{end} 合計：{sum(result_values)}")
    plt.pie(result_values, labels=result_keys, counterclock=False, startangle=90, autopct="%1.1f%%")
    plt.show()
