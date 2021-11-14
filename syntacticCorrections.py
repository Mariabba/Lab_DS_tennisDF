"""PRE-PROCESSING AND UNDERSTANDING"""
import pandas as pd
import pycountry as pc
from pathlib import Path

# Check the csv input file

"""Countries_ceck"""

df = pd.read_csv("data/inputs/countries.csv")
print(df.info())
df_1 = pd.read_csv("data/inputs/countryinfo.tsv", sep="\t")

print("Values in countries.csv, column counrty_name: \n" ,df['country_name'].unique())

print("Value in  countryinfo.tsv , column Country  :\n",df_1['Country'].unique())

null_data = df[df.isnull().any(axis=1)]

print(" Modify the values on the basis of that one that are in Country for having exact matching : ")
df['country_name'] = df['country_name'].replace(['Urugay','New Zeland','United States of America','Great Britain', 'North Macedonia'],[ 'Uruguay', 'New Zealand','United States','United Kingdom','Macedonia'])

print(df['country_name'].unique())

df.to_csv("data/work/countries_corrected.csv",index=False)


###Save
df_tennis = pd.read_csv("data/inputs/tennis.csv",low_memory = False)

cols_winner = ["winner_hand", "winner_ht"]
df_tennis.loc[:, cols_winner,] = df_tennis.groupby('winner_id')[cols_winner].ffill()

df_tennis.to_csv("data/work/tennis_adj.csv",index=False)