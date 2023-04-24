
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt

def visualization1(df):
    sns.histplot(x=df['species'])
    plt.xticks(rotation=90)
    plt.title('Shark species vs number of attacks')
    plt.xlabel('shark species')
    plt.ylabel('attacks')
    plt.show()


def visualization2(df):
    sharks = df["species"].value_counts()
    sharks.plot.pie(autopct="%.1f%%");
    plt.show()


def visualization3(df):
    sns.histplot(data=df, x="species", hue="fatality", multiple="stack");
    plt.xticks(rotation=90);
    plt.title('Shark species vs number of attacks and fatality')
    plt.xlabel('shark species')
    plt.ylabel('attacks');
    plt.show()