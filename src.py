import pandas as pd
import re


def basic_cleaning():
    #modificamos los espacios blancos en los titulos de las las columnas por añadimos _
    df.applymap(lambda x: x.lower() if type(x) == str else x)
    df.columns = [i.lower().replace(" ", "_") for i in df.columns]

    return df

def cleaning_df1():
    
    df1=df.copy()
    df.dropna(subset=['date', 'type', 'country', 'area', 'location', 'activity', 'sex_', 'species_', ], how='all')
    df1.rename(columns={'species_': 'species'}, inplace=True)
    
    return df1

def cleaning_df2():
    df_no_dates= df1.drop(['case_number', 'date','year'], axis=1)
    df2=df_no_dates.copy()
    
    return df2

def cleaning_df3():
    df_species=df2.dropna(subset=['species'])
    df3=df_species.copy()
    #deletting anything that's not a letter
    df3['species2'] = df3['species'].apply(lambda x: re.sub(r'\W+', ' ', x))
    #It searches for any numeric character (\d) followed by an optional character (.) and removes it
    df3['species2']=df3['species2'].apply(lambda x: re.sub(r'\d.?', '', x, flags=re.IGNORECASE))
    
    return df3

species_values=['white', 'nurse', 'blacktip', 'tiger', 'wobbegong', 'bull', 'blacktip', 'hammerhead', 'Mako', 'lemon', 'blacktip or spinner shark', 'largeako', 'oceanic whitetip', 'bronze whaler', 'spinner', 'caribbean reef', 'blue pointer', 'blue shark' ]

not_involved= ['Shark involvement prior to death unconfirmed', 'Shark involvement prior to death not confirmed' ]

def species_cleaning():
    
    for case in not_involved:
        df3.drop((df3['species2'] == case).index)

    #modificamos las celdas donde aparece una especie
    for specie in species_values:
        mask = df3['species2'].str.contains(specie, case=False)
        df.loc[mask, 'species2'] = specie
        
    
    return df3
