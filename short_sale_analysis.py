import pandas as pd
import pprint

from component.download_update import download_update


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

# TODO: Make Componentize and Add Market
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
            category = self.df[(self.df["コード"] == int(code))]["33業種区分"].tolist()
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

    def market(self, codes: list) -> dict:
        df_data = dict(self.df["市場・商品区分"].value_counts())
        df_keys = [k for k in df_data.keys()]

        result = {k: 0 for k in df_keys}

        for code in codes:
            markets = self.df[(self.df["コード"] == int(code))]["市場・商品区分"].tolist()
            try:
                result[markets[0]] += 1
            except IndexError as e:
                print(f"Error: {code} | {e}")

        return result

# download_update()

with open("./data/short_sale_codes.txt", "r", encoding="utf-8") as f:
    codes = [int(code.rstrip()) for code in f]

ca = CategoryAcquisition()

result = ca.acquisition(codes, rate=False)
"""
[('情報・通信業', 352),
 ('サービス業', 335),
 ('小売業', 225),
 ('電気機器', 199),
 ('卸売業', 191),
 ('化学', 162),
 ('機械', 156),
 ('建設業', 104),
 ('不動産業', 89),
 ('食料品', 88),
 ('銀行業', 76),
 ('輸送用機器', 67),
 ('医薬品', 65),
 ('その他製品', 64),
 ('金属製品', 47),
 ('陸運業', 44),
 ('繊維製品', 40),
 ('ガラス・土石製品', 38),
 ('精密機器', 38),
 ('鉄鋼', 34),
 ('-', 33),
 ('その他金融業', 30),
 ('倉庫・運輸関連業', 28),
 ('非鉄金属', 27),
 ('証券、商品先物取引業', 26),
 ('電気・ガス業', 22),
 ('パルプ・紙', 14),
 ('ゴム製品', 12),
 ('保険業', 10),
 ('海運業', 9),
 ('石油・石炭製品', 9),
 ('水産・農林業', 8),
 ('鉱業', 6),
 ('空運業', 3)]
"""

# result = ca.market(codes)
"""
[('市場第一部（内国株）', 2137),
 ('マザーズ（内国株）', 220),
 ('JASDAQ(スタンダード・内国株）', 145),
 ('市場第二部（内国株）', 96),
 ('ETF・ETN', 22),
 ('JASDAQ(グロース・内国株）', 19),
 ('REIT・ベンチャーファンド・カントリーファンド・インフラファンド', 11),
 ('マザーズ（外国株）', 1)]
"""

pprint.pprint(ranking(delete_empty(result)))