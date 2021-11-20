import pandas as pd
import missingno as msn
import matplotlib.pyplot as plt
import seaborn as sns


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


df_pla = pd.read_csv("data/players.csv")
print(df_pla.info())
print(missing_values_table(df_pla), "\n")

df_pla = df_pla.rename(columns={'country_id': 'country_code'})
print(df_pla.info())

"""Analisi countries.csv"""
df_geo = pd.read_csv("data/countries.csv")
print(df_geo.info())




# Tratto country_code  che non compaiono in countries.csv ma ci sono in players
df_treat = df_pla.merge(df_geo[['country_code', 'country_name']], on='country_code', how='left')
print(df_treat.head())

print(missing_values_table(df_treat), "\n")
null = df_treat[['country_name', 'country_code']][df_treat[['country_name', 'country_code']].isnull().any(axis=1)]
print(null)

print("colonne da riempire con UNK ", null['country_code'].unique())

df_pla = df_pla.replace(to_replace=['QAT', 'TTO', 'LBN', 'AZE', 'BRN', 'JAM', 'GHA', 'JOR', 'MRN', 'SYR', 'UAE', 'AHO'
    , 'BEN', 'ERI', 'ITF', 'COD', 'LBA', 'TKM', 'BER', 'SMR', 'ANT', 'TOG', 'VIN', 'BOT',
                                    'ZAM', 'SAU', 'BGR', 'LVA', 'CRI', 'BAN'], value='UNK')



#aggiungo la riga UNK per i codici errati a countries

UNK_row = {'country_code': 'UNK', 'country_name': 'Unknown', 'continent': 'Unknown', 'language': 'Unknown'}
df_geo = df_geo.append(UNK_row, ignore_index=True)

print(df_geo[120:])
