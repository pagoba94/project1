import pandas as pd
import re
import seaborn as sns
import os
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
vis.species_vs_total_attacks(df)
vis.species_vs_attacks_pie(df)
vis.species_vs_attacks_fatality(df)
vis.fatality_sex(df)
vis.species_vs_fatality(df)