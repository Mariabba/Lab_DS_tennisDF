import pandas as pd
import missingno as msn
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/z_player.csv")
print(df.info())

msn.matrix(df.sample(5))
plt.show()

print(df[' name'].unique())
print(df[' name'].value_counts())

print(df[' hand'].unique())
print(df[' hand'].value_counts())




