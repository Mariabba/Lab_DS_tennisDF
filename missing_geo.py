import pandas as pd
import missingno as msn
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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


df_geo = pd.read_csv("data/countries.csv")
print(df_geo.info())

msn.matrix(df_geo)
#plt.show()

print(missing_values_table(df_geo),"\n")

null_data = df_geo[df_geo.isnull().any(axis=1)]
print("Righe di geo con missing value \n ", null_data,"\n")


#df_geo = df_geo.astype({"country_code": str})

#df_geo_new = df_geo.astype(str)

df_geo = df_geo.astype({'continent': str})
#df_geo["continet"] = df_geo["continent"].apply(lambda x: str(x))
print(df_geo.info())

