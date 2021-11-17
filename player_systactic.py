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

null_player = df_pla[df_pla.isnull().any(axis=1)]
print("Righe di players con missing value \n ", null_player, "\n")

# elimino ht
print("Elimino ht")
df_pla = df_pla.drop(['ht'], axis=1)

# Converto il tipo delle  colonne in stringhe
df_pla = df_pla.convert_dtypes()
print(df_pla.info())
print(missing_values_table(df_pla), "\n")

df_pla.at[
    [2, 27, 62, 63, 102, 160, 189, 200, 201, 208, 244, 337, 344, 526, 550, 558, 791, 827, 838, 839, 854, 873, 897, 1034,
     1036, 4499, 4693, 5905], 'gender'] = 'M'

df_pla.at[[1897, 3180], 'gender'] = 'F'

print(missing_values_table(df_pla), "\n")

# Trattp hand : decidiamo di fare la moda e fill i 33 missing value
as_ser = df_pla['hand']
print("Mode of hand", as_ser.mode())

df_pla['hand'] = df_pla['hand'].fillna(value='U')

print(missing_values_table(df_pla), "\n")

# Tratto yob
print(df_pla[df_pla['yob'].isnull()])

df_pla = df_pla.fillna(value='Unknown')

print(missing_values_table(df_pla), "\n")

# Analisi del name

# sto analizzando se ci sono nomi che iniziano con formalismi

str = 'Mr', 'Miss', 'Ms', 'master', 'mr', 'ms', 'miss'
results = df_pla['name'].str.startswith(str)
print("Ci sono nomi che inizano con formalismi? :", results.unique())
