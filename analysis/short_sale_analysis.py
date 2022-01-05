import sys

sys.path.append("../")
from component.analizer import Analizer


with open("../data/short_sale_codes.txt", "r", encoding="utf-8") as f:
    codes = [int(code.rstrip()) for code in f]

analizer = Analizer(codes)

category_result = analizer.category()
market_result = analizer.market()

print(category_result)
print(market_result)
