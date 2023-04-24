import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
import src.downloading as dl
import src.cleaning as cl
import src.visualization as vis


df = dl.downloading('data/attacks.csv')
df = cl.basic_cleaning(df)
df = cl.cleaning_df1(df)
df = cl.cleaning_df2(df)
df = cl.species_cleaning(df)
df = cl.type_species_cleaning(df)
df = cl.fatality_sex_cleaning(df)
df = cl.visualization_cleaning(df)
df = vis.visualization1(df)
df = vis.visualization2(df)
df = vis.visualization3(df)