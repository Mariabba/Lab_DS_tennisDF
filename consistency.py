import csv
from pathlib import Path

from rich import print
from rich.console import Console
from rich.table import Table

mainfile = Path("data/tennis.csv")

with open(mainfile) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        for i, miao in enumerate(row.items()):
            print(f"{i}: {miao}")
        break  # I'm lazy but this should be improved before delivery

with open(mainfile) as csvfile:
    header = csvfile.readline().split(sep=",")
    print(header)
    header_len = len(header)

col_to_check_integrality = set(header[24:47])

st = {}
st["tot_values"] = 0
st["missing"] = 0
st["tot_rows"] = 0

best_of_set = set()
with open(mainfile) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        st["tot_rows"] += 1
        # let's check all rows are actually header_len (= 49) attributes long.
        assert len(row) == header_len
        # we also check that `tourney_date` is in the format YYYYMMDD for all rows
        assert len(str(row["tourney_date"])) == 8
        for key, val in row.items():
            # contiamo quanti values ci sono in tutto
            st["tot_values"] += 1
            # contiamo quanti missing values ci sono
            if len(val) == 0:
                st["missing"] += 1
            # controlliamo se la colonna è integer (solo se è una delle colonne in "col_to_check_integrality")
            if key in col_to_check_integrality and val:
                assert row[key] == f"{int(round(float(row[key])))}.0"
        # let's check how many unique values "best_of" has
        if row["best_of"] not in best_of_set:
            best_of_set.add(row["best_of"])

shape = (st["tot_rows"], header_len)

# start of visualization
table = Table(title=f"Statistics for {mainfile}")
table.add_column("Shape", justify="left", style="cyan")
table.add_column("Total values", justify="right", style="green")
table.add_column("Missing values", justify="right", style="cyan")
table.add_column("Missing values %", justify="right", style="green")
table.add_column("`best_of` unique", justify="right", style="cyan")
table.add_row(
    f"{shape[0]} rows\n{shape[1]} columns.",
    f"{st['tot_values']} (including the missing)",
    f"{st['missing']}",
    f"{round(st['missing']/st['tot_values']*100)}%",
    f"{best_of_set}",
)
console = Console()
console.print(table)
# end of visualization
