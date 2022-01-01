import pandas as pd

from .data_acquisition import data_acquisition


# TODO: I don't like something about it.

# bb: Bollinger Band
def bb_counter(code) -> dict:
    data = {}

    df = data_acquisition(code)
    bb = pd.DataFrame()

    bb["close"] = df["Close"]
    bb["mean"] = df["Close"].rolling(window=20).mean()
    bb["std"] = df["Close"].rolling(window=20).std()

    for sd in range(1, 4):
        bb[f"upper{sd}"] = bb["mean"] + (bb["std"] * sd)
        bb[f"lower{sd}"] = bb["mean"] - (bb["std"] * sd)

    for sd in range(1, 3):
        for close, upper, lower in zip(bb["close"][-1:], bb[f"upper{sd}"][-1:], bb[f"lower{sd}"][-1:]):
            if upper <= close:
                data[code] = sd
            if lower >= close:
                data[code] = -sd

    return data