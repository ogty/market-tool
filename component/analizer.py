import pandas as pd
import inspect


class Analizer:
    def __init__(self, codes: list, rate=False, n=3, err=False, ranking=True, ranking_reverse=True, delete_empty=True) -> None:
        df = pd.read_csv("./data/data_j.csv")
        self.df = df

        self.codes = codes
        self.rate = rate
        self.n = n
        self.err = err
        self.ranking = ranking
        self.ranking_reverse = ranking_reverse
        self.delete_empty = delete_empty

    def _ranking(self, data: dict) -> dict:
        result = sorted(data.items(), key=lambda x:x[1], reverse=self.ranking_reverse)
        return dict(result)

    def _delete_empty(self, data: dict) -> dict:
        result = {}
        for k, v in data.items():
            if v != 0:
                result[k] = v

        return result

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

    def category(self) -> dict:
        return self.common()

    def market(self) -> dict:
        return self.common()

    def common(self) -> dict:
        caller = str(inspect.stack()[1].function)

        if caller == "category":
            target = "33業種区分"
        elif caller == "market":
            target = "市場・商品区分"

        df_data = dict(self.df[target].value_counts())
        df_keys = [k for k in df_data.keys()]

        result = {k: 0 for k in df_keys}

        for code in self.codes:
            markets = self.df[(self.df["コード"] == int(code))][target].tolist()
            try:
                result[markets[0]] += 1
            except IndexError as e:
                if self.err:
                    print(f"Error: {code} | {e}")
                else:
                    pass
        
        if self.rate:
            result = {k: round(v / df_data[k], self.n) for k, v in result.items()}

        if self.delete_empty:
            result = self._delete_empty(result)

        if self.ranking:
            result = self._ranking(result)

        return result