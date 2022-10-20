from statistics import median
from typing import List

import numpy as np
import pandas as pd
from yahoo_finance_api2 import share


class HistoricalVolatirity:

    def __init__(self, code: str or int) -> None:
        self.code = code
        self.start_date = None
        self.end_date = None

    def stock_data(self) -> List[float]:
        my_share = share.Share("%s.T" % self.code)
        symbol_data = my_share.get_historical(
            share.PERIOD_TYPE_MONTH, 3,
            share.FREQUENCY_TYPE_DAY, 1
        )
        data = pd.DataFrame(symbol_data.values(), index=symbol_data.keys()).T
        timestamp = data["timestamp"].tolist()
        start_date = pd.to_datetime(timestamp[0], unit="ms")
        end_date = pd.to_datetime(timestamp[-1], unit="ms")
        self.start_date = start_date.strftime("%Y/%m/%d")
        self.end_date = end_date.strftime("%Y/%m/%d")

        data = data.close.astype(float).tolist()
        data.reverse()

        return data

    def rolling_window(self, data: List[float], window: int) -> np.ndarray:
        shape = data.shape[:-1] + (data.shape[-1] - window + 1, window)
        strides = data.strides + (data.strides[-1],)

        return np.lib.stride_tricks.as_strided(data, shape=shape, strides=strides)

    def calc(self, n: int = None, m: int = None) -> float:
        n = 20 if n is None else n
        m = 240 if m is None else m

        close = self.stock_data()
        data = np.array(close)
        rate = np.log(data[1:] / data[0: -1])
        std = np.hstack((
            np.empty(n) * np.nan,
            np.std(self.rolling_window(rate, n), axis=1, ddof=1),
        ))
        hv = (std * np.sqrt(m) * 100).tolist()

        return median(hv)


if __name__ == "__main__":
    hv = HistoricalVolatirity(7203)
    print(hv.calc())
    print(hv.start_date, hv.end_date)
