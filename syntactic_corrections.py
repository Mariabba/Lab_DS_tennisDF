"""PRE-PROCESSING"""
import pandas as pd
import pycountry as pc
from pathlib import Path

# Correggo gli errori sintattici di countries

#
df = pd.read_csv("data/inputs/countries.csv")
print(df.info())
df_1 = pd.read_csv("data/inputs/countryinfo.tsv", sep="\t")

print("Valori in counrty_name: \n" ,df['country_name'].unique())

print("valori in country info :\n",df_1['Country'].unique())

null_data = df[df.isnull().any(axis=1)]

print("Modifico i valori errati sulla base di quelli che sono riportati in country_info: ")
df['country_name'] = df['country_name'].replace(['Urugay','New Zeland','United States of America','Great Britain', 'North Macedonia'],[ 'Uruguay', 'New Zealand','United States','United Kingdom','Macedonia'])



print(df['country_name'].unique())

df.to_csv("data/work/countries_corrected.csv",index=False)
