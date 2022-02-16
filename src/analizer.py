import inspect
import os
from typing import List, Dict 

import pandas as pd

from settings import DATA_DIR


class Analizer:
    
    def __init__(
        self, 
        codes: List[str or int], 
        rate: bool = False, 
        n: int = None, 
        err: bool = False, 
        ranking: bool = True, 
        ranking_reverse: bool = True, 
        delete_empty: bool = True
    ) -> None:
        df = pd.read_csv(os.path.join(DATA_DIR, "data_j.csv"))
        self.df = df

        self.codes = codes
        self.rate = rate
        self.n = 3 if n is None else n
        self.err = err
        self.ranking = ranking
        self.ranking_reverse = ranking_reverse
        self.delete_empty = delete_empty

    def _ranking(self, data: Dict[str, float]) -> Dict[str, float]:
        result = sorted(data.items(), key=lambda x:x[1], reverse=self.ranking_reverse)
        return dict(result)

    def _delete_empty(self, data: Dict[str, float]) -> Dict[str, float]:
        result = {}
        for k, v in data.items():
            if v != 0:
                result[k] = v

        return result

    def distribution(self, *markets) -> Dict[str, int]:
        df_data = dict(self.df["33業種区分"].value_counts())
        result = {k: 0 for k in df_data.keys()}

        if markets:
            for market in markets:
                tmp_df = self.df[(self.df["市場・商品区分"] == market)]
                tmp_df_data = dict(tmp_df["33業種区分"].value_counts())

                for k, v in tmp_df_data.items():
                    result[k] += v
        else:
            tmp_df_data = dict(self.df["33業種区分"].value_counts())
            result = df_data

        return result

    def category(self) -> Dict[str, float]:
        return self.common()

    def market(self) -> Dict[str, float]:
        return self.common()

    def common(self) -> Dict[str, float]:
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
