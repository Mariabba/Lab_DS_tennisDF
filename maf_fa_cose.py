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


# Analisi Data.csv
df_data = pd.read_csv("data/dates.csv")
print(df_data.info())

msn.matrix(df_data)
plt.show()
print(missing_values_table(df_data))

# Analisi Geography.csv

df_geo = pd.read_csv("data/countries.csv")
print(df_geo.info())

msn.matrix(df_geo)
plt.show()
print(missing_values_table(df_geo),"\n")

null_data = df_geo[df_geo.isnull().any(axis=1)]
print("Righe di geo con missing value \n ", null_data,"\n")

#print(df_geo.isnull().sum().sort_values(ascending = False))

print("")
print("")
#Analisi Plyers
df_pla = pd.read_csv("data/players.csv")
print(df_pla.info())
print(missing_values_table(df_pla),"\n")

null_player = df_pla[df_pla.isnull().any(axis=1)]
print("Righe di players con missing value \n ", null_player,"\n")

"""

##Analisi tournament
df_trn = pd.read_csv("data/tournaments.csv")
print(df_trn.info())
print(missing_values_table(df_trn),"\n")

#Analisi Match
df_mtc = pd.read_csv("data/matches.csv")
print(df_mtc.info())
print(missing_values_table(df_mtc),"\n")


print(df[' name'].unique())
print(df[' name'].value_counts())

print(df[' hand'].unique())
print(df[' hand'].value_counts())
"""
