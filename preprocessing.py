"""PRE-PROCESSING AND UNDERSTANDING"""
import pandas as pd
import pycountry as pc
from pathlib import Path

# Check the csv input file

"""Countries_ceck"""

df = pd.read_csv("data/inputs/countries.csv")
print(df.info())
df_1 = pd.read_csv("data/inputs/countryinfo.tsv", sep="\t")

print("Values in countries.csv, column counrty_name: \n", df['country_name'].unique())

print("Value in  countryinfo.tsv , column Country  :\n", df_1['Country'].unique())

null_data = df[df.isnull().any(axis=1)]

print(" Modify the values on the basis of that one that are in Country for having exact matching : ")
df['country_name'] = df['country_name'].replace(
    ['Urugay', 'New Zeland', 'United States of America', 'Great Britain', 'North Macedonia'],
    ['Uruguay', 'New Zealand', 'United States', 'United Kingdom', 'Macedonia'])

print(df['country_name'].unique())

df.to_csv("data/work/countries_corrected.csv", index=False)

"""
###Saverio per correggere altezza
df_tennis = pd.read_csv("data/inputs/tennis.csv", low_memory=False)

cols_winner = ["winner_hand", "winner_ht"]

df_tennis.loc[:, cols_winner, ] = df_tennis.groupby('winner_id')[cols_winner].bfill()

df_tennis.to_csv("data/work/tennis_adj.csv", index=False)
"""




# aggiusto in tennis i loser rank e winner rank (con save)
df_tennis = pd.read_csv("data/inputs/tennis.csv")
print(df_tennis.info())

cols_rank_winner = ["winner_rank", "winner_rank_points"]
cols_rank_loser = ["loser_rank", "loser_rank_points"]


df_tennis.loc[:, cols_rank_winner] = df_tennis.sort_values(by="tourney_date").groupby('winner_id')[
    cols_rank_winner].bfill()
df_tennis.loc[:, cols_rank_winner] = df_tennis.sort_values(by="tourney_date").groupby('winner_id')[
    cols_rank_winner].ffill()
df_tennis.loc[:, cols_rank_loser] = df_tennis.sort_values(by="tourney_date").groupby('loser_id')[
    cols_rank_loser].bfill()
df_tennis.loc[:, cols_rank_loser] = df_tennis.sort_values(by="tourney_date").groupby('loser_id')[
    cols_rank_loser].ffill()

print(df_tennis[["tourney_level", "winner_rank", "winner_rank_points"]].groupby("tourney_level").agg(
    {'winner_rank': ['mean', 'size'], 'winner_rank_points': ['mean', 'size']}).sort_values(by=("winner_rank", "mean")))

df_tennis["winner_rank"] = df_tennis[["winner_rank", "tourney_level"]].fillna(value=mean_rank_level["winner_rank", "mean"])["winner_rank"]