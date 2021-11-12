import csv
from pathlib import Path

from rich import print
from rich.console import Console
from rich.progress import track
from rich.table import Table


def extract_header(mainfile: Path, table: str) -> list:
    """
    Takes the mainfile Path object and a table string (table = 'tournament' | 'player' | 'match')
    Returns a list of columns that can be used as header of a csv file, appropriate with `table`
    """
    with open(mainfile) as csvfile:
        header = csvfile.readline()[:-1].split(sep=",")
    if table == "tournament":
        return header[0:6] + header[47:49]
    if table == "player_winner":
        return [header[7]] + header[9:14] + [header[5]]
    if table == "player_loser":
        return [header[14]] + header[16:21] + [header[5]]
    if table == "match":
        return ["match_id"] + [header[0]] + header[6:8] + [header[14]] + header[21:47]


def extract_table(
    mainfile: Path, file: Path, header: list, len_mainfile: int = 186073
) -> set:
    console.log(f"Extracting {file}\nwith header: {header}…")
    ids = set()
    with open(file, mode="w") as target:
        if "tournament" in file.stem:
            # changing column name "tourney_date" to "date_id"
            my_header = header[0:5] + ["date_id"] + header[6:]
            target.write(f"{','.join(my_header)}\n")
            with open("data/log.md", mode="a") as log:
                log.write(f"- `{file}` has {my_header}.\n")

        else:
            target.write(f"{','.join(header)}\n")
        with open(mainfile) as source:
            id = -1
            for row in track(csv.DictReader(source), total=len_mainfile):
                # only add if unique
                to_app = ""
                if "tournament" in file.stem:
                    id = row["tourney_id"]
                elif "match" in file.stem:
                    id += 1
                    to_app = f"{to_app},{id}"
                else:
                    raise Exception("oops")
                if id not in ids:  # id is NOT already written in csv
                    ids.add(id)
                    for row_key, value in row.items():
                        # add only the columns that are required in table
                        if row_key in header:
                            # start of value-wise transformations
                            pass
                            to_app = f"{to_app},{value}"
                    # row-wise transformations start here
                    pass
                    # transform ioc into country_id here
                    pass
                    # add gender here
                    pass
                    target.write(f"{to_app[1:]}\n")  # [1:] to eliminate the first comma
    console.log(f"Wrote to {file} {len(ids)} unique rows.")
    return ids


# let's create the tables schemas
mainfile = Path("data/inputs/tennis.csv")
len_mainfile = 186073
paths = {}
paths["tournament"] = Path("data/tournaments.csv")
paths["player"] = Path("data/work/players.csv")
paths["match"] = Path("data/matches.csv")
console = Console()

# make Player table
file = paths["player"]
header_winner = extract_header(mainfile, "player_winner")
header_loser = extract_header(mainfile, "player_loser")
header = ["tourney_date", "player_id", "name", "hand", "ht", "country_id", "age"]

console.log(f"Extracting {file}\nwith header: {header}…")
ids = set()
with open(file, mode="w") as target:
    target.write(f"{','.join(header)}\n")
    with open(mainfile) as source:
        for row in track(csv.DictReader(source), total=len_mainfile):
            # only add if unique (winner)
            id = row["winner_id"]
            if id not in ids:  # id is NOT already written in csv
                ids.add(id)
                to_app = ""
                for row_key, value in row.items():
                    # add only the columns that are required in table
                    if row_key in header_winner:  # <- care _winner
                        # if ht and ht exists, cast to int
                        if row_key == "winner_ht" and value:
                            to_app = f"{to_app},{round(float(value))}"
                        else:
                            to_app = f"{to_app},{value}"
                # transform ioc into country_id here
                pass
                # add gender here
                pass
                target.write(f"{to_app[1:]}\n")

            # only add if unique (loser)
            id = row["loser_id"]
            if id not in ids:
                ids.add(id)
                to_app = ""
                for row_key, value in row.items():
                    # add only the columns that are required in table
                    if row_key in header_loser:  # <- care _loser
                        # if ht and ht exists, cast to int
                        if row_key == "loser_ht" and value:
                            to_app = f"{to_app},{round(float(value))}"
                        else:
                            to_app = f"{to_app},{value}"
                # transform ioc into country_id here
                pass
                # add gender here
                pass
                target.write(f"{to_app[1:]}\n")  # [1:] to eliminate the first comma
console.log(f"Wrote to {file} {len(ids)} unique rows.")

# start testing
console.log(f"Testing {file}…")
from pandas import read_csv

# did we write the csvs correctly?
assert len(ids) == len(read_csv(file))
# did we get as many unique rows as source?
loser_ids = read_csv(mainfile, low_memory=False)["loser_id"]
assert len(ids) == len(
    read_csv(mainfile, low_memory=False)["winner_id"]
    .append(loser_ids, ignore_index=True)
    .unique()
)
console.log(f"Tests done on {file}.")
# end testing

# make Tournament table
file = paths["tournament"]
header = extract_header(mainfile, "tournament")
ids = extract_table(mainfile, file, header, len_mainfile)

# start testing
console.log(f"Testing {file}…")
# did we write the csvs correctly?
assert len(ids) == len(read_csv(file))
# did we get as many unique rows as source?
assert len(ids) == len(read_csv(mainfile, low_memory=False)["tourney_id"].unique())
console.log(f"Tests done on {file}.")
# end testing


# make Matches table
file = paths["match"]
header = extract_header(mainfile, "match")
ids = extract_table(mainfile, file, header, len_mainfile)
# I did not put testing here
