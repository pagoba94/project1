import pandas as pd
import re

def downloading(df):
    """This function downloads from a raw link and saves the dataframe locally.
    args:
    :url: string. the link
    :name: string. name to save the file
    """
    import pandas as pd
    df=pd.read_csv('data/attacks.csv', encoding='latin')
    
    return df

def basic_cleaning(df):
    #modificamos los espacios blancos en los titulos de las las columnas por añadimos _
    df= df.applymap(lambda x: x.lower() if type(x) == str else x)
    df= df.columns = [i.lower().replace(" ", "_") for i in df.columns]

    return df

def cleaning_df1(df):
    
    df1=df.copy()
    df.dropna(subset=['date', 'type', 'country', 'area', 'location', 'activity', 'sex_', 'species_', ], how='all')
    df1.rename(columns={'species_': 'species'}, inplace=True)
    
    return df1

def cleaning_df2(df):
    df_no_dates= df1.drop(['case_number', 'date','year'], axis=1)
    df2=df_no_dates.copy()
    
    return df2

def cleaning_df3(df):
    df_species=df2.dropna(subset=['species'])
    df3=df_species.copy()
    #deletting anything that's not a letter
    df3['species2'] = df3['species'].apply(lambda x: re.sub(r'\W+', ' ', x))
    #It searches for any numeric character (\d) followed by an optional character (.) and removes it
    df3['species2']=df3['species2'].apply(lambda x: re.sub(r'\d.?', '', x, flags=re.IGNORECASE))
    
    
    return df3


def species_cleaning(df):
    species_values=['white', 'nurse', 'blacktip', 'tiger', 'wobbegong', 'bull', 'blacktip', 'hammerhead', 'Mako', 'lemon', 'blacktip or spinner shark', 'largeako', 'oceanic whitetip', 'bronze whaler', 'spinner', 'caribbean reef', 'blue pointer', 'blue shark' ]
    not_involved= ['Shark involvement prior to death unconfirmed', 'Shark involvement prior to death not confirmed', 'Shark involvement suspected but not confirmed', 'Invalid']
    
    for case in not_involved:
        df3.drop((df3['species2'] == case).index)

    #modificamos las celdas donde aparece una especie
    for specie in species_values:
        mask = df3['species2'].str.contains(specie, case=False)
        df.loc[mask, 'species2'] = specie
        
    #elimina las letras m y a si se encuentran fuera de palabras
    df3['species2'].str.replace(r'\s[m|a]\s', ' ', regex=True)
    df3['species2'].str.replace(r'^m|a\s', '', regex=True)
    df3['species2'].str.replace(r'\sm|as$', '', regex=True)
    
    #eliminamos las palabras con dos letras de toda la columna
    df3['species2'].apply(lambda x: ' '.join([word for word in x.split() if len(word) > 2]))
    
    return df3
