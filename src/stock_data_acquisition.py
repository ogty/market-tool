import datetime

import pandas as pd
from yahoo_finance_api2 import share


def data_acquisition(code: str or int) -> pd.DataFrame:
    columns = ["Dates", "High", "Low", "Close", "Volume"]
    dates = []

    my_share = share.Share(f"{code}.T")
    symbol_data = my_share.get_historical(share.PERIOD_TYPE_DAY, 2, share.FREQUENCY_TYPE_MINUTE, 5)

    data = pd.DataFrame(symbol_data.values(), index=symbol_data.keys()).T

    for ts in data.timestamp:
        dates.append(datetime.datetime.fromtimestamp(ts / 1000))

    dates = pd.Series(dates)

    df = pd.concat([dates, data.high, data.low, data.close, data.volume], axis=1)
    df.columns = columns
    df = df.reset_index()
    df = df.drop("index", axis=1)

    # ymd: year month day
    latest_date = str(df["Dates"][0])
    latest_ymd = latest_date.split(' ')[0]
    one_day_ago = int(latest_ymd.split('-')[-1]) - 1

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month

    result = df[df["Dates"] >= datetime.datetime(year, month, one_day_ago)]
    result = df.dropna(how="any")

    return result
