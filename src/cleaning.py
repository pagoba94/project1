import pandas as pd
import re

def basic_cleaning(df):
    #modificamos todas las letras a minúsculas
    df=df.applymap(lambda x: x.lower() if type(x) == str else x)
    #modificamos los espacios blancos en los titulos de las las columnas por añadimos _
    df.columns = [i.lower().replace(" ", "_") for i in df.columns]
    #drops all rows from DataFrame "df" that contain all missing values (NaN)
    df = df.dropna(how='all')
    #eliminamos duplicados
    df= df.drop_duplicates()
    
    return df


def cleaning_df1(df):
    
    #creates a copy of the principal df named df1
    #eliminamos las columnas indicadas del df1
    df.drop(['case_number', 'date', 'year', 'area', 'location', 'activity', 'name','investigator_or_source','pdf','href_formula', 'href', 'case_number.1', 'case_number.2', 'unnamed:_22','unnamed:_23' ], axis=1, inplace=True)
    ##creamos una copia de la columna species
    df['species2']=df['species_'].copy()
    #eliminamos todas las filas de las columnas indicadas con duplicados
    df.drop_duplicates() 
    #drops all rows from df1 that contain all missing values (NaN) in the specified subset of columns ('type', 'fatal_(y/n)', 'species2') and modifies the DataFrame in place.
    df.dropna(subset=['type', 'fatal_(y/n)', 'species2'], how='all', inplace=True)
    #rename some columns
    df.rename(columns={'species_': 'species1', 'fatal_(y/n)':'fatality', 'sex_' : 'sex'}, inplace=True)
    
    return df



def cleaning_df2(df):
      
    # Eliminar las filas con valores NaN en la columna species2
    df.dropna(subset=['species2'], how='all', inplace=True)
    
    #It searches for any numeric character (\d) followed by an optional character (.) and removes it
    df['species2']=df['species2'].apply(lambda x: re.sub(r'\d.?', '', x, flags=re.IGNORECASE))
    
    #deletting anything that's not a letter
    df['species2'] = df['species2'].apply(lambda x: re.sub(r'\W+', ' ', x))
    
    return df 


def species_cleaning(df):
    
    #removes the letters 'm' and 'a' if they are found out of words.
    df['species2'] = df['species2'].str.replace(r'\s[m|a]\s', ' ', regex=True)
    df['species2'] = df['species2'].str.replace(r'^m|a\s', '', regex=True)
    df['species2'] = df['species2'].str.replace(r'\sm|as$', '', regex=True)
    
    #drops rows from df where the value in the 'species2' column is equal to any string in the "not_involved" list.
    not_involved= ['Shark involvement prior to death unconfirmed', 'shark involvement not confirmed', 'shark involvement no t confirmed', 'Shark involvement prior to death not confirmed', 'Shark involvement suspected but not confirmed', 'Invalid', 'shark involvement not confirmed']
    for case in not_involved:
        df.drop(df[df['species2'] == case].index)
    
    #creamos un diccionario con los tipos de especies y los valores con los que aparece en el dataset
    species_dict={'white shark': 'white shark|whites', 
                  'nurse shark': 'nurse|nurses',
                  'tiger shark': 'tiger|tigers',
                  'grey reef shark': 'grey|greys|gray',
                  'wobbegong shark':'wobbegong|wobbegongs',
                  'bull shark': 'bull|bulls|zambezi|zambesi',
                  'blacktip shark': 'blacktip|blacktips|black tipped',
                  'hammerhead shark': 'hammerhead|hammerheads', 
                  'mako shark': 'Mako|Makos|ako|Akos',
                  'lemon shark': 'lemon|lemons',
                  'largeako shark': 'largeako|largeakos', 
                  'oceanic whitetip shark': 'oceanic whitetip|oceanic whitetips', 
                  'whitetip reef shark':'whtietip|white tipped|whitetip reef',
                  'bronze whaler shark': 'bronze whaler|bronze whalers|bronze whale|Copper', 
                  'spinner shark': 'spinner|spinners',                 
                  'caribbean reef shark' : 'caribbean reef|caribbean reefs',                  
                  'blue shark' : 'blue pointer|blue pointers|blue shark|blue sharks|blue nose', 
                  'sandbar shark': 'brown|brown sharks|sand|sandbar',
                  'raggedtooth shark': 'raggedtooth',
                  'dog fish shark': 'dog|dogfish',                
                  'unidentified shark' : 'unidentified|unknown',
                  'small shark' : 'small shark|small sharks'
                 }
    
    # Itera sobre cada elemento de la columna species2 del dataframe y reemplaza los valores
    for key, value in species_dict.items():
        mask= df['species2'].str.contains(value, case=False)
        df.loc[mask, 'species2'] = key

    #modificamos las celdas donde aparece una especie
    for specie, word in species_dict.items():   
        df.loc[df['species2'].str.contains(word, case=False), 'species2'] = specie
    
    
    #keeps only the words with more than two characters and then joins them back together with spaces
    df['species2'] = df['species2'].apply(lambda x: ' '.join([word for word in x.split() if len(word) > 2]))
    
    
    
    return df


def type_species_cleaning(df):

    #drops rows from df where the value in the 'type' column is equal to 'invalid', and modifies the df3.
    df.drop(df[df['type'] =='invalid'].index, inplace=True)
    
    #we eliminate rows with species2 column with Nan 
    df.dropna(subset=['species2'], how='all', inplace=True)
    
    #we remove the unique values that have less than 6 elements on the species2 column in df
    species_counts= {}
    for i,x in df['species2'].value_counts().items():
        species_counts[i]=x
        
    new_dict = {}
        
    for key, value in species_counts.items():
        if type(value) == int:
            if value >= 6:
                new_dict[key] = value

    
    #we remove those unique values that are not shark species
    species_list = list(new_dict.keys())
    species_list.remove('shark')
    species_list.remove('')
    species_list.remove('sharks')
    species_list.remove('small shark')
    species_list.remove('unidentified shark')
    species_list.remove('shark involvement not confirmed')
    
    df = df[df['species2'].isin(species_list)]
    
    
    df.drop(['age', 'time'], axis=1, inplace=True)

    return df


def fatality_sex_cleaning(df):
    #modificamos los datos de la columna fatality
    mask_unknown = (df['fatality'] == '2017')
    
    # Reemplazar las palabras en las filas seleccionadas
    df.loc[mask_unknown, 'fatality'] = 'unknown'
    
    #modificamos los datos de la columna fatality
    mask_no = (df['fatality'] == ' n')
    
    # Reemplazar las palabras en las filas seleccionadas
    df.loc[mask_no, 'fatality'] = 'n'
    
    #modificamos los datos de la columna fatality
    mask_unknown2 = (df['fatality'] == 'm')
    
    # Reemplazar las palabras en las filas seleccionadas
    df.loc[mask_unknown2, 'fatality'] = 'unknown'
    
    df['sex']=df['sex'].str.replace(r'm\s', 'm', regex=True)
    df['sex']=df['sex'].str.replace(r'n', 'unknown', regex=True)
    df['sex']=df['sex'].str.replace(r'lli', 'unknown', regex=True)
    
    return df


def visualization_cleaning(df):
    #creamos un df con la variable especies y fatality
    df = df.loc[:, ['species2', 'fatality']]
    df.rename(columns={'species2': 'species'}, inplace=True)
    
    #modificamos los datos de la columna fatality por integers
    no_fatality = (df['fatality'] == 'n')
    # Reemplazar las palabras en las filas seleccionadas
    df.loc[no_fatality, 'fatality'] = 0
    
    #modificamos los datos de la columna fatality por integers
    yes_fatality = (df['fatality'] == 'y')
    # Reemplazar las palabras en las filas seleccionadas
    df.loc[yes_fatality, 'fatality'] = 1
    
    return df