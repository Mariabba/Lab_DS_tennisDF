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


df_mtc = pd.read_csv("data/matches.csv")
print(df_mtc.info())
print(missing_values_table(df_mtc), "\n")

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

print(missing_values_table(df_mtc), "\n")


# Converto il tipo delle  colonne in stringhe
df_mtc['tourney_id'] = df_mtc['tourney_id'].convert_dtypes()
df_mtc['score'] = df_mtc['score'].convert_dtypes()
df_mtc['round'] = df_mtc['round'].convert_dtypes()
print(df_mtc.info())

