import pandas as pd
import pycountry as pc
import pycountry_convert as pcc
#from dataprep.clean import clean_country


# Correggo gli errori sintattici di countries

df = pd.read_csv("data/inputs/countries.csv")
print(df.info())
df_1 = pd.read_csv("data/inputs/countryinfo.tsv",sep = "\t")

print(df['country_name'].unique())

#clean_country(df, "country_name")
#clean_country(df_1,"Country")

# metto i nomi in una lista upper case così posso fare la comparazione
input_c_name_list = list(df['country_name'])
input_c_name_list = [element.upper() for element in input_c_name_list]

inpu2 = list(df_1['Country'])
inpu2 = [element.upper() for element in inpu2]


# funzione

def country_name_check(in_list):
    pycntrlst = list(pc.countries)
    name = []
    common_name = []
    official_name = []
    invalid_countryname = []
    tobe_deleted = ['IRAN', 'SOUTH KOREA', 'SUDAN', 'MACAU', 'REPUBLIC OF IRELAND']

    for i in pycntrlst:
        name.append(i.name)
        if hasattr(i, 'common_name'):
            common_name.append(i.common_name)
        else:
            common_name.append("")
        if hasattr(i, 'official_name'):
            official_name.append(i.official_name)
        else:
            official_name.append("")

    for j in in_list:
        if  j not in map(str.upper,name) and j not in map(str.upper, common_name) and j not in map(str.upper, official_name):
            invalid_countryname.append(j)
    invalid_countryname = list(set(invalid_countryname))
    invalid_countryname = [item for item in invalid_countryname if item not in tobe_deleted]

    return print(invalid_countryname)

print ("\nLista country errate nel csv:")
country_name_check(input_c_name_list)

print ("\nLista country errate nel tsv:")
country_name_check(inpu2)

cn_name = pcc.convert_country_name_to_country_alpha2(input_c_name_list )
pprint(cn_name)
