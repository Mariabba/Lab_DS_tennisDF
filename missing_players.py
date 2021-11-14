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
print(missing_values_table(df_pla),"\n")

null_player = df_pla[df_pla.isnull().any(axis=1)]
print("Righe di players con missing value \n ", null_player,"\n")


#elimino ht
print("Elimino ht")
df_pla = df_pla.drop(['ht'], axis = 1)


#Converto il tipo delle  colonne in stringhe
df_pla = df_pla.convert_dtypes()
print(df_pla.info())
print(missing_values_table(df_pla),"\n")

#Tratto gender

#Trattp hand

#Tratto yob