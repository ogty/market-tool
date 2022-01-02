import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib


def df_slicer(df: pd.DataFrame, k: int) -> list:
    n = df.shape[0]
    dfs = [df.loc[i:i + k - 1, :] for i in range(0, n, k)]

    return dfs

def ranking(data: dict, reverse=True) -> dict:
    return sorted(data.items(), key=lambda x:x[1], reverse=reverse)

def delete_empty(data: dict) -> dict:
    result = {}
    for k, v in data.items():
        if v != 0:
            result[k] = v
    return result

class CategoryAcquisition:
    def __init__(self) -> None:
        df = pd.read_csv("./data/data_j.csv")
        df_data = dict(df["33業種区分"].value_counts())
        df_keys = [k for k in df_data.keys()]

        self.df = df
        self.df_data = df_data
        self.result = {k: 0 for k in df_keys}

    def distribution(self, *markets) -> dict:
        if markets:
            for market in markets:
                tmp_df = self.df[(self.df["市場・商品区分"] == market)]
                df_data = dict(tmp_df["33業種区分"].value_counts())

                for k, v in df_data.items():
                    self.result[k] += v
        else:
            df_data = dict(self.df["33業種区分"].value_counts())
            self.result = df_data

        return self.result

    def acquisition(self, codes: list, rate=True, n=3, err=False) -> dict:
        for code in codes:
            category = self.df[(self.df["コード"] == code)]["33業種区分"].tolist()
            try:
                self.result[category[0]] += 1
            except IndexError as e:
                if err:
                    print(f"Error: {code} | {e}")
                else:
                    pass
        if rate:
            self.result = {k: round(v / self.df_data[k], n) for k, v in self.result.items()}

        return self.result

ca = CategoryAcquisition()

# print(ca.distribution("市場第一部（内国株）", "マザーズ（内国株）"))

df_up = pd.read_csv("./market_data/1/2_up.csv")
splited_dfs = df_slicer(df_up, 100)


for i, splited_df in enumerate(splited_dfs[:]):
    start = str(i * 100 + 1).rjust(4)
    end = str((i + 1) * 100).rjust(4)
    
    print(f"{start} ~ {end}")
    result = ca.acquisition(splited_df["code"], rate=False)
    result = dict(ranking(delete_empty(result)))
    print(result)

    result_keys = [k for k in result.keys()]
    result_values = [v for v in result.values()]

    plt.title(f"{start}〜{end} 合計：{sum(result_values)}")
    plt.pie(result_values, labels=result_keys, counterclock=False, startangle=90, autopct="%1.1f%%")
    plt.show()
