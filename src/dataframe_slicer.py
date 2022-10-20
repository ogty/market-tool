from typing import List

import pandas as pd


def df_slicer(df: pd.DataFrame, k: int) -> List[pd.DataFrame]:
    n = df.shape[0]
    dfs = [df.loc[i:i + k - 1, :] for i in range(0, n, k)]

    return dfs
