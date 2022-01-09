import os
import re


TOP_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(TOP_DIR, "data")
LOGS_DIR = os.path.join(DATA_DIR, "logs")
IMAGES_DIR = os.path.join(TOP_DIR, "images")
MARKET_DATA_DIR = os.path.join(DATA_DIR, "market_data")
TOTALLING_DATA_DIR = os.path.join(DATA_DIR, "totalling_data")

RE_MAX_PAGE_NUM = re.compile(r"...(?P<max_page_num>[\d]+)次へ")
RE_UP_DENOMINATOR = re.compile(r"/(?P<up_denominatro>[\d]+)件中")
