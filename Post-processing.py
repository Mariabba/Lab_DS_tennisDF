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

msn.matrix(df_geo)
plt.show()
print(missing_values_table(df_geo),"\n")

null_data = df_geo[df_geo.isnull().any(axis=1)]
print("Righe di geo con missing value \n ", null_data,"\n")

#Riscrivo la riga Poc
df_geo = df_geo.drop([107])
POC_row = {'country_code' : 'POC','country_name':'Pacific Oceania','continent':'Oceania', 'language' : 'En'}
df_geo = df_geo.append(POC_row,ignore_index=True)

#controllo che sia tutto okay
null_data_1 = df_geo[df_geo.isnull().any(axis=1)]
print("Righe di geo con missing value \n ", null_data_1,"\n")

#Converto il tipo delle  colonne in stringhe
df_geo = df_geo.convert_dtypes()
print(df_geo.info())

#risalvo il dataframe
df_geo.to_csv("data/countries.csv",index=False)



#Analisi Tournaments.csv
df_trn = pd.read_csv("data/tournaments.csv")
print(df_trn.info())
print(missing_values_table(df_trn),"\n")

#Converto il tipo delle  colonne in stringhe
df_trn = df_trn.convert_dtypes()
print(df_trn.info())

#Fill surface
null_data = df_trn[df_trn.isnull().any(axis=1)]
print("Righe di geo con missing value \n ", null_data,"\n")

print(df_trn.loc[[2089]])

#abbiamo osservato che in tornei con nomi simili che dovrebbero essere lo stesso,
# i materiali del surface sono diversi fra loro, quindi non possiamo concludee che le righe che sembrano essere lo
# stesso torneo siano lo stesso materiale di surface, Quindi facciamo la mediana

serie = df_trn['surface']
print(serie.mode())
df_trn['surface'] = df_trn['surface'].fillna(value ='Hard')

print(missing_values_table(df_trn),"\n")

#risalvo il dataframe
df_trn.to_csv("data/tournaments.csv",index=False)





