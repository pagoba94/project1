import pandas as pd
import re

def basic_cleaning(df):
    """This function modifies all words to lowercase, modifies the spaces in the column titles (replaces spaces with "_"),
    removes all rows with all NaN values, and removes duplicates.
    args: df
    return: df. cleaned df
    """
    
    #modifies all words to lowercase
    df=df.applymap(lambda x: x.lower() if type(x) == str else x)
    #modifies the spaces in the column titles (replaces spaces with "_"
    df.columns = [i.lower().replace(" ", "_") for i in df.columns]
    #drops all rows from DataFrame "df" that contain all missing values (NaN)
    df = df.dropna(how='all')
    #removes duplicates
    df= df.drop_duplicates()
    
    return df


def cleaning_df1(df):
    """This function #remove the indicated columns from the df, creates a copy of the species_ column called species2,
    remove all rows from the indicated columns with duplicates, drops all rows from df that contain all missing values (NaN)
    in the specified subset of columns ('type', 'fatal_(y/n)', 'species2') and modifies the DataFrame in place. And renames some columns.
    args: df
    return: df. cleaned df
    """
    
    #remove the indicated columns from the df
    df.drop(['case_number', 'date', 'year', 'area', 'location', 'activity', 'name','investigator_or_source','pdf','href_formula', 'href', 'case_number.1', 'case_number.2', 'unnamed:_22','unnamed:_23' ], axis=1, inplace=True)
    #create a copy of the species_ column called species2
    df['species2']=df['species_'].copy()
    #remove all rows from the indicated columns with duplicates.
    df.drop_duplicates() 
    #drops all rows from df that contain all missing values (NaN) in the specified subset of columns ('type', 'fatal_(y/n)', 'species2') and modifies the DataFrame in place.
    df.dropna(subset=['type', 'fatal_(y/n)', 'species2'], how='all', inplace=True)
    #rename some columns
    df.rename(columns={'species_': 'species', 'fatal_(y/n)':'fatality', 'sex_' : 'sex'}, inplace=True)
    
    return df



def cleaning_df2(df):
    """This function rops all rows from df that contain all missing values (NaN) in the specified subset of column ('species2')
    and modifies the DataFrame in place. It searches on the column ('species2')for any numeric character (\d) followed by an optional character (.) and 
    removes it, as well as deletes anything that's not a letter.
    args: df
    return: df. cleaned df
    """
    #drops all rows from df that contain all missing values (NaN) in the specified subset of column ('species2') and modifies the DataFrame in place.
    df.dropna(subset=['species2'], how='all', inplace=True)
    
    #It searches for any numeric character (\d) followed by an optional character (.) and removes it
    df['species2']=df['species2'].apply(lambda x: re.sub(r'\d.?', '', x, flags=re.IGNORECASE))
    
    #deletes anything that's not a letter
    df['species2'] = df['species2'].apply(lambda x: re.sub(r'\W+', ' ', x))
    
    return df


def species_cleaning(df):
    """This function modifies column species2, removes the letters 'm' and 'a' if they are found out of words,
    drops rows from df where the value in the 'species2' column is equal to any string in the "not_involved" list, 
    creates a dictionary with the species types and the values they appear with in the dataset, Iterates over each element
    of the species2 column of the dataframe and replace the values for the keys, and keeps only the words with more than two
    characters and then joins them back together with spaces
    args: df
    return: df. cleaned df
    """
    
    #removes the letters 'm' and 'a' if they are found out of words.
    df['species2'] = df['species2'].str.replace(r'\s[m|a]\s', ' ', regex=True)
    df['species2'] = df['species2'].str.replace(r'^m|a\s', '', regex=True)
    df['species2'] = df['species2'].str.replace(r'\sm|as$', '', regex=True)
    
    #drops rows from df where the value in the 'species2' column is equal to any string in the "not_involved" list.
    not_involved= ['Shark involvement prior to death unconfirmed', 'shark involvement not confirmed', 'shark involvement no t confirmed', 'Shark involvement prior to death not confirmed', 'Shark involvement suspected but not confirmed', 'Invalid', 'shark involvement not confirmed']
    for case in not_involved:
        df.drop(df[df['species2'] == case].index)
    
    #create a dictionary with the species types and the values they appear with in the dataset
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
    
    # Iterate over each element of the species2 column of the dataframe and replace the values for the keys
    for key, value in species_dict.items():
        mask= df['species2'].str.contains(value, case=False)
        df.loc[mask, 'species2'] = key

    #modify the cells where a species appears.
    for specie, word in species_dict.items():   
        df.loc[df['species2'].str.contains(word, case=False), 'species2'] = specie
    
    #keeps only the words with more than two characters and then joins them back together with spaces
    df['species2'] = df['species2'].apply(lambda x: ' '.join([word for word in x.split() if len(word) > 2]))
    
    return df



def type_species_cleaning(df):
    """This function drops rows from df where the value in the 'type' column is equal to 'invalid', and modifies the df.
    eliminate rows with species2 column with Nan, removes the unique values that have less than 6 elements on the species2
    column in df, remove those unique values that are not shark species. drops age and time columns from the df.
    args: df
    return: df. cleaned df
    """
    
    #drops rows from df where the value in the 'type' column is equal to 'invalid', and modifies the df.
    df.drop(df[df['type'] =='invalid'].index, inplace=True)
    
    #eliminate rows with species2 column with Nan 
    df.dropna(subset=['species2'], how='all', inplace=True)
    
    #remove the unique values that have less than 6 elements on the species2 column in df
    species_counts= {}
    for i,x in df['species2'].value_counts().items():
        species_counts[i]=x
        
    new_dict = {}
        
    for key, value in species_counts.items():
        if type(value) == int:
            if value >= 6:
                new_dict[key] = value

    
    #remove those unique values that are not shark species
    species_list = list(new_dict.keys())
    species_list.remove('shark')
    species_list.remove('')
    species_list.remove('sharks')
    species_list.remove('small shark')
    species_list.remove('unidentified shark')
    species_list.remove('shark involvement not confirmed')
    
    df = df[df['species2'].isin(species_list)]
    
    #drops age and time columns from the df
    df.drop(['age', 'time'], axis=1, inplace=True)

    return df


def fatality_sex_cleaning(df):
    """This function modifies specified data in the fatality column an Replaces words in the selected rows.
    args: df
    return: df. cleaned df
    """
    #modify the data in the fatality column
    mask_unknown = (df['fatality'] == '2017')
    
    #Replace the words in the selected rows
    df.loc[mask_unknown, 'fatality'] = 'unknown'
    
    #modify the data in the fatality column
    mask_no = (df['fatality'] == ' n')
    
    #Replace the words in the selected rows
    df.loc[mask_no, 'fatality'] = 'n'
    
    #modify the data in the fatality columny
    mask_unknown2 = (df['fatality'] == 'm')
    
    #Replace the words in the selected rows
    df.loc[mask_unknown2, 'fatality'] = 'unknown'
    
    df['sex']=df['sex'].str.replace(r'm\s', 'm', regex=True)
    df['sex']=df['sex'].str.replace(r'n', 'unknown', regex=True)
    df['sex']=df['sex'].str.replace(r'lli', 'unknown', regex=True)
    
    return df


def visualization_cleaning(df):
    """This function modifies specified data in the fatality column an Replaces words in the selected rows to yes or no.
    args: df
    return: df. cleaned df
    """
    
    #create a df with the variables species, sex, and fatality
    df = df.loc[:, ['species2', 'fatality','sex']]
    df.rename(columns={'species2': 'species'}, inplace=True)
    
    
    #modify the data in the fatality column to yes or no
    no_fatality = (df['fatality'] == 'n')
    df.loc[no_fatality, 'fatality'] = "no"
    
    yes_fatality = (df['fatality'] == 'y')
    df.loc[yes_fatality, 'fatality'] = "yes"
    
    
    return df