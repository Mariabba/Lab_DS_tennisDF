import csv
from pathlib import Path

import pyodbc
from rich.console import Console
from rich.progress import track


def open_conn():
    server = "tcp:131.114.72.230"  # lds.di.unipi.it ?
    database = "Group_4_DB"
    username = "Group_4"
    password = "6VEKJ00D"
    connectionString = (
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + server
        + ";DATABASE="
        + database
        + ";UID="
        + username
        + ";PWD="
        + password
    )
    cn = pyodbc.connect(connectionString)
    return cn, cn.cursor()


def close_conn(cn, cursor):
    cursor.close()
    cn.close()


def load_table(name: str, my_path: Path, csv_len: int):
    # 1. open connection to server
    cn, cursor = open_conn()

    # 2. load table into memory
    with open(my_path) as source:
        reader = csv.DictReader(source)

        # 3. write table onto server, row by row? Remember the data-types
        for row in track(reader, total=csv_len, description=f"{name}…"):
            query = f"INSERT INTO {name} VALUES {[value for value in row.values()]}"
            cursor.execute(query)

    # 4. close connection
    close_conn(cn, cursor)


console = Console()
tables = {}

tables["geography"] = (Path("data/countries.csv"), 124)
tables["dates"] = (Path("data/dates.csv"), 375)
tables["matches"] = (Path("data/matches.csv"), 186073)
tables["players"] = (Path("data/players.csv"), 10074)
tables["tournaments"] = (Path("data/tournaments.csv"), 4853)

console.log(f"Loading…")

for name, path_and_len in tables.items():
    load_table(name, path_and_len[0], csv_len=path_and_len[1])

console.log(f"Loaded {len(tables)} tables onto server.")
