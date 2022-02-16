from typing import List, Dict 

import pandas as pd

from .stock_data_acquisition import data_acquisition


# bb: Bollinger Band
# std: Standard Diviation
def bb_counter(codes: List[int or str]) -> Dict[int or str, float]:
    data = {}
    for code in codes:
        df = data_acquisition(code)
        bb = pd.DataFrame()

        bb["close"] = df["Close"]
        bb["mean"] = df["Close"].rolling(window=20).mean()
        bb["std"] = df["Close"].rolling(window=20).std()

        for std in range(1, 4):
            bb[f"upper{std}"] = bb["mean"] + (bb["std"] * std)
            bb[f"lower{std}"] = bb["mean"] - (bb["std"] * std)

        for std in range(1, 3):
            for close, upper, lower in zip(bb["close"][-1:], bb[f"upper{std}"][-1:], bb[f"lower{std}"][-1:]):
                if upper <= close:
                    data[code] = std
                if lower >= close:
                    data[code] = -std

    return data
