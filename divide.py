import csv
from pathlib import Path

# we use read_csv() only to check that our solutions are correct.
from pandas import read_csv
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
        header = csvfile.readline().split(sep=",")
    if table == "tournament":
        result_header = header[0:5] + header[47:49]
    if table == "player_winner":
        result_header = [header[7]] + header[9:13]
    if table == "player_loser":
        result_header = [header[14]] + header[16:20]
    if table == "match":
        result_header = [header[0]] + [header[7]] + [header[14]] + header[21:47]
    return result_header


# let's create the tables schemas
mainfile = Path("data/tennis.csv")
len_mainfile = 186073
paths = {}
paths["tournament"] = Path("data/z_tournament.csv")
paths["player"] = Path("data/z_player.csv")
paths["match"] = Path("data/z_match.csv")
console = Console()

# make Player table
file = paths["player"]
header_winner = extract_header(mainfile, "player_winner")
header_loser = extract_header(mainfile, "player_loser")
header = ["id", "name", "hand", "ht", "ioc"]

console.log(f"Extracting {file}\nwith header: {header}")
ids = set()
# for csv_key, path in paths.items():
with open(file, mode="w") as target:
    target.write(f"{', '.join(header)}\n")
    with open(mainfile) as source:
        for row in track(csv.DictReader(source), total=len_mainfile):
            # check unique ID of winner
            id = row["winner_id"]
            if id not in ids:  # id is NOT already written in csv
                ids.add(id)
                to_app = ""
                for row_key, value in row.items():
                    # add only the columns that are required in table
                    if row_key in header_winner:  # <- care _winner
                        if not to_app:
                            to_app = value
                        else:
                            to_app = f"{to_app},{value}"
                target.write(f"{to_app}\n")

            # check unique ID of loser
            id = row["loser_id"]
            if id not in ids:
                ids.add(id)
                to_app = ""
                for row_key, value in row.items():
                    # add only the columns that are required in table
                    if row_key in header_loser:  # <- care _loser
                        if not to_app:
                            to_app = value
                        else:
                            to_app = f"{to_app},{value}"
                target.write(f"{to_app}\n")
console.log(f"Wrote to {file} {len(ids)} unique rows")
# testing
assert len(ids) == len(read_csv(file))
