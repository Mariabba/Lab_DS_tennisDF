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


""" Analisi Data.csv """
df_data = pd.read_csv("data/dates.csv")
print(df_data.info())
print(df_data.head())

msn.matrix(df_data)
plt.show()
print(missing_values_table(df_data))

"""Analisi countries.csv"""
df_geo = pd.read_csv("data/countries.csv")
print(df_geo.info())

msn.matrix(df_geo)
plt.show()
print(missing_values_table(df_geo), "\n")

null_data = df_geo[df_geo.isnull().any(axis=1)]
print("Righe di geo con missing value \n ", null_data, "\n")

# Riscrivo la riga Poc
df_geo = df_geo.drop([107])
POC_row = {'country_code': 'POC', 'country_name': 'Pacific Oceania', 'continent': 'Oceania', 'language': 'En'}
df_geo = df_geo.append(POC_row, ignore_index=True)

#Rinomino il country code del kosovo che è sbagliato
df_geo= df_geo.replace(to_replace ='UNK',value = 'RKS')

#aggiungo la riga UNK per i codici errati che ci potrebbero essere in altre tabelle

UNK_row = {'country_code': 'UNK', 'country_name': 'Unknown', 'continent': 'Unknown', 'language': 'Unknown'}
df_geo = df_geo.append(UNK_row, ignore_index=True)

print(df_geo[120:])

# controllo che sia tutto okay
null_data_1 = df_geo[df_geo.isnull().any(axis=1)]
print("Righe di geo con missing value \n ", null_data_1, "\n")

# Converto il tipo delle  colonne in stringhe
df_geo = df_geo.convert_dtypes()
print(df_geo.info())

# risalvo il csv
df_geo.to_csv("data/countries.csv", index=False)

"""Analisi Tournaments.csv"""
df_trn = pd.read_csv("data/tournaments.csv")
print(df_trn.info())
print(missing_values_table(df_trn), "\n")

# Converto il tipo delle  colonne in stringhe
df_trn = df_trn.convert_dtypes()
print(df_trn.info())

# Fill surface
null_data = df_trn[df_trn.isnull().any(axis=1)]
print("Righe di geo con missing value \n ", null_data, "\n")

print(df_trn.loc[[2089]])

# abbiamo osservato che in tornei con nomi simili che dovrebbero essere lo stesso,
# i materiali del surface sono diversi fra loro, quindi non possiamo concludee che le righe che sembrano essere lo
# stesso torneo siano lo stesso materiale di surface, Quindi facciamo la mediana

surface = df_trn['surface']
print(surface.mode())
df_trn['surface'] = df_trn['surface'].fillna(value='Hard')

print(missing_values_table(df_trn), "\n")

# risalvo il csv
df_trn.to_csv("data/tournaments.csv", index=False)

"""Analisi players.csv"""
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

# Tratto gender
# questa prima linea stampa le rows senza gender
print(df_pla[df_pla['gender'].isnull()])

# identifico quali sono i nomi e ci assegno M o F

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

# Tratto country_code  che non compaiono in countries.csv ma ci sono in players
df_pla = df_pla.rename(columns={'country_id': 'country_code'}) #rinomino country_id in country_code
df_treat = df_pla.merge(df_geo[['country_code', 'country_name']], on='country_code', how='left') #merge con country_code
print(df_treat.head())

 # ora so che ci sono 68 codici che non compaiono in countries
null = df_treat[['country_name', 'country_code']][df_treat[['country_name', 'country_code']].isnull().any(axis=1)]
print(null)

print("colonne da riempire con UNK ", null['country_code'].unique())

df_pla = df_pla.replace(to_replace=['QAT', 'TTO', 'LBN', 'AZE', 'BRN', 'JAM', 'GHA', 'JOR', 'MRN', 'SYR', 'UAE', 'AHO'
    , 'BEN', 'ERI', 'ITF', 'COD', 'LBA', 'TKM', 'BER', 'SMR', 'ANT', 'TOG', 'VIN', 'BOT',
                                    'ZAM', 'SAU', 'BGR', 'LVA', 'CRI', 'BAN'], value='UNK') #rimpiazzo con UNK

# risalvo il csv
print(df_pla.info())
df_pla.to_csv("data/players.csv", index=False)

"""Analisi matches.csv"""

df_mtc = pd.read_csv("data/matches.csv", low_memory = False)
print(df_mtc.info())

df_mtc = df_mtc.convert_dtypes()
# print(missing_values_table(df_mtc), "\n")

# Riempio score & minutes 681
df_mtc['score'] = df_mtc['score'].fillna(value='Unknown')

df_mtc['minutes'] = df_mtc['minutes'].fillna(value=-1)

# Riempio l_ e w_

df_mtc['l_df'] = df_mtc['l_df'].fillna(value=-1)
df_mtc['l_bpFaced'] = df_mtc['l_bpFaced'].fillna(value=-1)
df_mtc['l_2ndWon'] = df_mtc['l_2ndWon'].fillna(value=-1)
df_mtc['l_1stWon'] = df_mtc['l_1stWon'].fillna(value=-1)
df_mtc['l_1stIn'] = df_mtc['l_1stIn'].fillna(value=-1)
df_mtc['l_svpt'] = df_mtc['l_svpt'].fillna(value=-1)
df_mtc['l_ace'] = df_mtc['l_ace'].fillna(value=-1)
df_mtc['l_bpSaved'] = df_mtc['l_bpSaved'].fillna(value=-1)
df_mtc['l_SvGms'] = df_mtc['l_SvGms'].fillna(value=-1)

df_mtc['w_df'] = df_mtc['w_df'].fillna(value=-1)
df_mtc['w_bpFaced'] = df_mtc['w_bpFaced'].fillna(value=-1)
df_mtc['w_2ndWon'] = df_mtc['w_2ndWon'].fillna(value=-1)
df_mtc['w_1stWon'] = df_mtc['w_1stWon'].fillna(value=-1)
df_mtc['w_1stIn'] = df_mtc['w_1stIn'].fillna(value=-1)
df_mtc['w_svpt'] = df_mtc['w_svpt'].fillna(value=-1)
df_mtc['w_ace'] = df_mtc['w_ace'].fillna(value=-1)
df_mtc['w_bpSaved'] = df_mtc['w_bpSaved'].fillna(value=-1)
df_mtc['w_SvGms'] = df_mtc['w_SvGms'].fillna(value=-1)

# print(missing_values_table(df_mtc), "\n")


# Converto il tipo delle  colonne in stringhe
df_mtc['tourney_id'] = df_mtc['tourney_id'].convert_dtypes()
df_mtc['score'] = df_mtc['score'].convert_dtypes()
df_mtc['round'] = df_mtc['round'].convert_dtypes()
print(df_mtc.info())

# risalvo il dataframe
df_mtc.to_csv("data/matches.csv", index=False)
