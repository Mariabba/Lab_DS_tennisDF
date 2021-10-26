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


col_to_check_integrality = set(header[24:47])


tot_counter = 0
counter = 0
tot_rows = 0
best_of_set = set()
with open(mainfile) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        tot_rows += 1
        # let's check all rows are actually header_len (= 49) attributes long.
        assert len(row) == header_len
        for key, val in row.items():
            # contiamo quanti values ci sono in tutto
            tot_counter += 1
            # contiamo quanti missing values ci sono
            if len(val) == 0:
                counter += 1
            # controlliamo se la colonna è integer (solo se è una delle colonne in "col_to_check_integrality")
            if key in col_to_check_integrality and val:
                assert row[key] == f"{int(round(float(row[key])))}.0"
        # let's check how many unique values "best_of" has
        if row["best_of"] not in best_of_set:
            best_of_set.add(row["best_of"])



print(f"In total, we have {counter} missing values through the entire {mainfile}, which by the way has {tot_counter} values all together.")

print(f"This accounts for a {round(counter/tot_counter*100)}% missing values.")

shape = (tot_rows, header_len)
print(f"There are {shape[0]} rows and {shape[1]} columns.")

print(f"How many best_of sets we have? {best_of_set}")

# let's create the tables schemas
