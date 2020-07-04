import requests
import os
from csv import DictReader
from io import StringIO

from local_hour import get_local_day_dates

RESCUETIME_API = "https://www.rescuetime.com/anapi/data"
RESCUETIME_API_KEY = os.environ['RESCUETIME_API_KEY']

# Columns
RANK_COL = "Rank"
TIME_COL = "Time Spent (seconds)"
CATEGORY_COl = "Category"

def format_seconds(seconds):
    strs = []
    if seconds>=3600:
        strs.append(f"{seconds//3600}h")
        seconds %= 3600
    if seconds >= 60:
        strs.append(f"{seconds//60}m")
    return " ".join(strs)

def parse_row(row):
    result_row = {}
    result_row["rank"] = int(row[RANK_COL])
    result_row["time"] = format_seconds(int(row[TIME_COL]))
    result_row["category"] = row[CATEGORY_COl]
    result_row["seconds"] = int(row[TIME_COL])
    return result_row

def get_rescuetime_data():
    day_start, day_end = get_local_day_dates()
    day_start_str = str(day_start)
    payload = {
        "key": RESCUETIME_API_KEY,
        "perspective": "rank",
        "restrict_begin": day_start_str,
        "format": "csv",
        "restrict_kind": "overview",
    }
    r = requests.get(RESCUETIME_API, params=payload)
    raw_data = StringIO(r.text)
    data = DictReader(raw_data, dialect="unix")
    result_data = [*map(parse_row, data)]
    result_data = [*filter(lambda x : x["rank"]<=5, result_data)]

    return result_data
