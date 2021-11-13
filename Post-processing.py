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
print(df_data.head())

msn.matrix(df_data)
plt.show()
print(missing_values_table(df_data))


#Analisi Geo.csv
df_geo = pd.read_csv("data/countries.csv")
print(df_geo.info())


print(missing_values_table(df_geo),"\n")

null_data = df_geo[df_geo.isnull().any(axis=1)]
print("Righe di geo con missing value \n ", null_data,"\n")


#Converto il tipo delle  colonne in stringhe
df_geo = df_geo.convert_dtypes()
print(df_geo.info())

#Converto Poc in Pacific Ocean e ci assegno la lingua
df_geo['country_name'] = df_geo['country_name'].replace(['nan'],['Pacific Oceania'])
df_geo['continent'] = df_geo['continent'].replace(['Unknown'],['Oceania'])
df_geo['language'] = df_geo['language'].replace(['NaN '],['En'])

#verifico che è tutto corretto
print(missing_values_table(df_geo),"\n")
