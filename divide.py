import csv
import datetime
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
        return ["match_id"] + [header[0]] + header[5:8] + [header[14]] + header[21:47]


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
                            if value and (row_key[:2] == "w_" or row_key[:2] == "l_"):
                                value = int(float(value))
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
mainfile = Path("data/work/tennis_adj.csv")
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

len_playersfile = 10074
males = Path("data/inputs/male_players.csv")
females = Path("data/inputs/female_players.csv")


def assign_gender(players: Path, males: Path, females: Path) -> None:
    """
    Takes 3 paths objects and adds the `gender` column to the `players` csv file.
    """
    target_file = Path("data/work/players_with_g.csv")
    with open("data/log.md", mode="a") as log:
        log.write(f"- `{target_file}` is with `gender`.\n")
    files = (males, females)
    sets = {}

    for gender_file in files:
        # create appropriate set for males and for females
        sets[gender_file.stem] = set()
        # for each file, males and females, …
        with open(gender_file) as source:
            for row in csv.DictReader(source):
                name = f"{row['name']} {row['surname']}"
                sets[gender_file.stem].add(name)
    console.log(f"Read gender from {files}.")

    female_count = 0
    missing_count = 0
    male_count = 0
    console.log(f"Writing `gender` into {target_file} of {len_playersfile} players…")
    with open(target_file, mode="w") as target:
        with open(players) as source:
            target.write(f"{source.readline()[:-1]},gender\n")
        with open(players) as source:
            for row in track(csv.DictReader(source), total=len_playersfile):
                to_app = ""
                for key, value in row.items():
                    to_app = f"{to_app},{value}"
                if row["name"] in sets[males.stem]:
                    to_app = f"{to_app},M"
                    male_count += 1
                elif row["name"] in sets[females.stem]:
                    to_app = f"{to_app},F"
                    female_count += 1
                else:
                    missing_count += 1
                    to_app = f"{to_app},"
                target.write(f"{to_app[1:]}\n")
    console.log(
        f"Wrote {male_count} male players and {female_count} female players with {missing_count} players of unknown gender."
    )


def assign_yob(players: Path):
    target_file = Path("data/players.csv")
    with open("data/log.md", mode="a") as log:
        log.write(
            f"- `{target_file}` is with `yob` (year of birth) and without `age`.\n"
        )
    with open(players) as source:
        reader = csv.DictReader(source)
        columns = [c for c in reader.fieldnames if c != "age"] + ["yob"]
        with open(target_file, mode="w") as target:
            writer = csv.DictWriter(target, fieldnames=columns)
            writer.writeheader()
            for row in reader:
                if row["age"] and row["tourney_date"]:
                    my_date = row["tourney_date"]
                    my_days = round(float(row["age"]) * 365)
                    row["yob"] = (
                        datetime.date(
                            year=int(my_date[:4]),
                            month=int(my_date[4:6]),
                            day=int(my_date[6:]),
                        )
                        - datetime.timedelta(days=my_days)
                    )
                del row["age"]
                writer.writerow(row)
    console.log(f"Wrote year of birth `yob` to {target_file} and deleted `age`.")


assign_gender(Path("data/work/players.csv"), males, females)
assign_yob(Path("data/work/players_with_g.csv"))


# make Geography table
additional = Path("data/inputs/countryinfo.tsv")
countries = Path("data/work/countries_corrected.csv")
countries_target = Path("data/countries.csv")

with open("data/log.md", mode="a") as log:
    log.write(
        f"- `{countries_target}` is with `language` (language **codes**) based on `country_name`.\n"
    )

languages_dict = {}
with open(additional) as adds:
    adds_reader = csv.DictReader(adds, delimiter="\t")
    for row in adds_reader:
        languages_dict[row["Country"]] = row["Languages"]
console.log(f"Read {len(languages_dict)} languages from {additional}.")

with open(countries_target, mode="w") as target:
    with open(countries) as source:
        reader = csv.DictReader(source)
        columns = reader.fieldnames + ["language"]
        writer = csv.DictWriter(target, fieldnames=columns)
        writer.writeheader()
        for row in reader:
            if row["country_name"] in languages_dict:
                row["language"] = languages_dict[row["country_name"]]
            else:
                row["language"] = None
            writer.writerow(row)
console.log(f"Wrote something to {countries_target}.")

# making Date and linking it with Tournaments
date_target = Path("data/dates.csv")
tournaments = Path("data/tournaments.csv")
dates_set = set()
console.log(f"Creating dates in {date_target} from {tournaments}.")
with open(date_target, mode="w") as target:
    with open(tournaments) as source:
        reader = csv.DictReader(source)
        columns = ["date_id", "day", "month", "quarter", "year"]
        writer = csv.DictWriter(target, fieldnames=columns)
        writer.writeheader()
        for row in reader:
            my_date = row["date_id"]
            if my_date not in dates_set:
                dates_set.add(my_date)
                to_write = {}
                to_write["date_id"] = my_date
                my_f_date = datetime.date(
                    year=int(my_date[:4]),
                    month=int(my_date[4:6]),
                    day=int(my_date[6:]),
                )
                to_write["day"] = my_f_date.day
                to_write["month"] = my_f_date.month
                to_write["year"] = my_f_date.year
                if my_f_date.month in [1, 2, 3]:
                    to_write["quarter"] = 1
                elif my_f_date.month in [4, 5, 6]:
                    to_write["quarter"] = 2
                elif my_f_date.month in [7, 8, 9]:
                    to_write["quarter"] = 3
                elif my_f_date.month in [10, 11, 12]:
                    to_write["quarter"] = 4
                else:
                    raise Exception
                writer.writerow(to_write)
console.log(f"Wrote {len(dates_set)} dates in {date_target}.")
with open("data/log.md", mode="a") as log:
    log.write(f"- `{date_target}` has {columns}.\n")
