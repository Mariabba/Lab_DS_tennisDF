import csv
from pathlib import Path

from rich import print
from rich.console import Console
from rich.progress import track
from rich.table import Table

len_playersfile = 10074
players = Path("data/work/players.csv")
males = Path("data/inputs/male_players.csv")
females = Path("data/inputs/female_players.csv")
console = Console()


def assign_gender(players: Path, males: Path, females: Path) -> tuple:
    """
    Takes 3 paths objects and returns a tuple of two int (int, int) representing how many
    males and how many females were found.
    """
    target_file = Path("data/players.csv")
    with open("data/log.md", mode="a") as log:
        log.write(f"{target_file} is with `gender`.\n")
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


assign_gender(players, males, females)

# make Geography table
additional = Path("data/inputs/countryinfo.tsv")
countries = Path("data/inputs/countries.csv")
countries_target = Path("data/countries.csv")

with open("data/log.md", mode="a") as log:
    log.write(
        f"{countries_target} is with `language` (language codes) based on `country_name`.\n"
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
