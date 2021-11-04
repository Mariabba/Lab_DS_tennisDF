from pandas import read_csv
from divide import *

# did we write the csvs correctly?
assert len(ids) == len(read_csv(file))

# did we get as many unique rows as source?
loser_ids = read_csv(mainfile, low_memory=False)["loser_id"]
assert len(ids) == len(
    read_csv(mainfile, low_memory=False)["winner_id"]
    .append(loser_ids, ignore_index=True)
    .unique()
)
