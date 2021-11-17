"""PRE-PROCESSING AND UNDERSTANDING"""
import pandas as pd
import pycountry as pc
from pathlib import Path

# Check the csv input file

"""Countries_ceck"""

df = pd.read_csv("data/inputs/countries.csv")
# print(df.info())
df_1 = pd.read_csv("data/inputs/countryinfo.tsv", sep="\t")

# print("Values in countries.csv, column counrty_name: \n", df['country_name'].unique())

# print("Value in  countryinfo.tsv , column Country  :\n", df_1['Country'].unique())

null_data = df[df.isnull().any(axis=1)]

# print(" Modify the values on the basis of that one that are in Country for having exact matching : ")
df['country_name'] = df['country_name'].replace(
    ['Urugay', 'New Zeland', 'United States of America', 'Great Britain', 'North Macedonia'],
    ['Uruguay', 'New Zealand', 'United States', 'United Kingdom', 'Macedonia'])

# print(df['country_name'].unique())

df.to_csv("data/work/countries_corrected.csv", index=False)




# aggiusto in tennis i loser rank e winner rank

def missing_values_table(df):
    mis_val = df.isnull().sum()
    mis_val_percent = 100 * df.isnull().sum() / len(df)
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
    mis_val_table_ren_columns = mis_val_table.rename(
        columns={0: 'Missing Values', 1: '% of Total Values'})
    mis_val_table_ren_columns = mis_val_table_ren_columns[
        mis_val_table_ren_columns.iloc[:, 1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)
    print("Il Dataframe ha " + str(df.shape[1]) + " colonne.\n"
                                                  "Ci sono " + str(mis_val_table_ren_columns.shape[0]) +
          " colonne che hanno missing value.")
    return mis_val_table_ren_columns


df_tennis = pd.read_csv("data/inputs/tennis.csv")

print(missing_values_table(df_tennis), "\n")

df_tennis.loc[:, "winner_rank"] = df_tennis.groupby(['tourney_level'])['winner_rank'].transform(
    lambda x: x.fillna(x.mean()))
df_tennis.loc[:, "winner_rank_points"] = df_tennis.groupby(['tourney_level'])['winner_rank_points'].transform(
    lambda x: x.fillna(x.mean()))
df_tennis.loc[:, "loser_rank"] = df_tennis.groupby(['tourney_level'])['loser_rank'].transform(
    lambda x: x.fillna(x.mean()))
df_tennis.loc[:, "loser_rank_points"] = df_tennis.groupby(['tourney_level'])['loser_rank_points'].transform(
    lambda x: x.fillna(x.mean()))

print(missing_values_table(df_tennis), "\n")

df_tennis.to_csv("data/work/tennis_corrected.csv", index=False)