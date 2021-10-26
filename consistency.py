from rich import print
from pathlib import Path
import csv

mainfile = Path("data/tennis.csv")

with open(mainfile) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        for i, miao in enumerate(row.items()):
            print(f"{i}: {miao}")
        break

with open(mainfile) as csvfile:
    header = csvfile.readline().split(sep=",")
    print(header)
    header_len = len(header)
    print(f"Our header is {header_len} attributes long.")

# let's check all rows are actually header_len (= 49) attributes long.

with open(mainfile) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        assert len(row) == header_len
