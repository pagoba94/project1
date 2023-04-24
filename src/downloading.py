
import pandas as pd

def downloading(path):
    """This function downloads from a raw link and saves the dataframe locally.
    args:
    :url: string. the link
    :name: string. name to save the file
    """
    
    df=pd.read_csv(path, encoding='latin')
    
    return df