from datetime import datetime
import json
from math import isnan
import os
import sys
import japanize_matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from src.historical_volatirity import HistoricalVolatirity


# ANSI color for error display
RED = "\033[31m"
NO_COLOR = "\033[0m"

today = datetime.today().strftime("%Y-%m-%d")
width, _ = os.get_terminal_size()
displayable_number = (width // 5) - 1

# Loads the issue codes of all listed issues
with open("./data/codes.txt", 'r', encoding="utf-8") as f:
    codes = [code.rstrip() for code in f.readlines()]


historical_volatirity = {}

# Use first data for period acquisition
first_data = codes[0]
hv = HistoricalVolatirity(first_data)
historical_volatirity[first_data] = hv.calc()
start_date = hv.start_date
end_date = hv.end_date

# Calculate, display and store historical volatility
display_count = 0
is_error = False
for code in codes[1:]:
    try:
        hv = HistoricalVolatirity(code).calc()
        # If historical volatility was NaN, it is set to 0.0
        historical_volatirity[code] = 0.0 if isnan(hv) else hv
    except Exception as error:
        is_error = True
    finally:
        code = "%s%s%s" % (RED, code, NO_COLOR) if is_error else code
        if display_count != displayable_number:
            print(code, end=' ')
            display_count += 1
        else:
            sys.stdout.write("%s\n" % code)
            display_count = 0

        sys.stdout.flush()
        is_error = False

# Save historical volatility as a json file
with open(f"./data/hv-{today}.json", 'w', encoding="utf-8") as f:
    json.dump(historical_volatirity, f, indent=4, ensure_ascii=False)


# Create and save a histogram of historical volatility
value_only_hv = [hv for hv in historical_volatirity.values()]
summary_statistics_for_hv = pd.DataFrame(pd.Series(value_only_hv).describe()).transpose()
labels = {
    "count": "サンプル数",
    "mean": "平均",
    "std": "標準偏差",
    "min": "最小値",
    "25%": "第一四分位数",
    "50%": "中央値",
    "75%": "第三四分位数",
    "max": "最大値",
}
maximum_length_of_label = 6
describe = ''
for en_label, ja_label in labels.items():
    ja_label_length = len(ja_label)
    if ja_label_length < maximum_length_of_label:
        ja_label += (maximum_length_of_label - ja_label_length) * '\u3000'
    describe += "%s\uFF1A%.2f\n" % (ja_label, float(summary_statistics_for_hv[en_label]))

figure = plt.figure()
plt.title(f"全上場銘柄のヒストリカルボラティリティ(HV)\n{start_date} 〜 {end_date}")
plt.xlabel("HV")
plt.ylabel("銘柄数")

plt.axvline(float(summary_statistics_for_hv["50%"]), color="#BFCC94", label="中央値")
plt.text(float(summary_statistics_for_hv["50%"]), 125, "───中央値", rotation=0, color="#BFCC94")

plt.axvline(float(summary_statistics_for_hv["mean"]), color="#F2B134", label="平均")
plt.text(float(summary_statistics_for_hv["mean"]), 100, "───平均", rotation=0, color="#F2B134")

plt.axvspan(
    float(summary_statistics_for_hv["25%"]),
    float(summary_statistics_for_hv["75%"]),
    color="#C492B1",
    label="四分位範囲",
)
plt.text(float(summary_statistics_for_hv["75%"]) - 1, 150, "──四分位範囲", rotation=0, color="#C492B1")

plt.hist(value_only_hv, bins=200, color="#344966", label="銘柄数")
plt.figtext(0.61, 0.55, describe, wrap=True, horizontalalignment="left", fontsize=11)
plt.savefig(f"./images/hv-{today}.png")
