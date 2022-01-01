import numpy as np
import statistics
import pandas as pd
from yahoo_finance_api2 import share


class HistoricalVolatirity:
    def __init__(self, code) -> None:
        self.code = code

    def stock_data(self) -> list:
        my_share = share.Share(f"{self.code}.T")
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_YEAR, 1, share.FREQUENCY_TYPE_DAY, 1)
        data = pd.DataFrame(symbol_data.values(), index=symbol_data.keys()).T
        data = list(data.close)
        data.reverse()

        return data

    def rolling_window(self, data, window) -> None:
        shape = data.shape[:-1] + (data.shape[-1] - window + 1, window)
        strides = data.strides + (data.strides[-1],)

        return np.lib.stride_tricks.as_strided(data, shape=shape, strides=strides)

    def calc(self, n=20, m=240) -> float:
        close = self.stock_data()
        data = np.array(close)
        rate = np.log(data[1:] / data[0:-1])
        std = np.hstack((np.empty(n) * np.nan, np.std(self.rolling_window(rate, n), axis=1, ddof=1)))
        hv = (std * np.sqrt(m) * 100).tolist()

        return hv