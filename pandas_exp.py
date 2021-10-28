from pathlib import Path

from rich import print

import pandas as pd

mainfile = Path("data/tennis.csv")

df = pd.read_csv(mainfile, low_memory=False)
print(len(df["winner_id"].unique()))
