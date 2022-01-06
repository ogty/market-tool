import os
import sys

sys.path.append("../")
from component.analizer import Analizer
from settings import DATA_DIR


with open(os.path.join(DATA_DIR, "short_sale_codes.txt"), "r", encoding="utf-8") as f:
    codes = [int(code.rstrip()) for code in f]

analizer = Analizer(codes)

category_result = analizer.category()
market_result = analizer.market()

print(category_result)
print(market_result)
