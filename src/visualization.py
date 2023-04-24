
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
import os

def species_vs_total_attacks(df):
    """This function Creates a countplot with species column in ascending order and with deep palette, Rotate x-axis 
    tick labels for better readability and modifies title, xlabel and ylabel. Finally it saves the plot as an image 
    called: species_vs_total_attacks
    args:
    -df: pandas DataFrame containing the shark attack data
    returns:
    -None
    """
    
    # Creates a countplot with species column in ascending order and with deep palette
    sns.countplot(y=df['species'], order=df['species'].value_counts(ascending=True).index, palette='deep')
    
    # Rotate x-axis tick labels for better readability and modifies title, xlabel and ylabel.
    plt.xticks(rotation=90)
    plt.title('26 shark species vs 1.860 attacks')
    plt.ylabel('Shark species', weight='bold')
    plt.xlabel('Number of attacks', weight='bold')
    
    # Save the plot as an image and display the plot
    plt.savefig('figures/species_vs_total_attacks.png')
    os.system("start figures/species_vs_total_attacks.png")
    plt.show()

def species_vs_attacks_pie(df):
    """This function Creates a pieplot with species column, Sum the counts of all species that make up less than 10% 
    of the total, Group these species into a new category called "Other" and save the plot as an image and display the plot.
    args:
    -df: pandas DataFrame containing the shark attack data
    returns:
    -None
    """
    sharks = df["species"].value_counts()
    # Sum the counts of all species that make up less than 10% of the total
    other_count = sharks[sharks/sum(sharks) < 0.04].sum()
    # Group these species into a new category called "Other"
    sharks = sharks[sharks/sum(sharks) >= 0.04]
    sharks["Other"] = other_count
    # Plot the pie chart
    
    sharks.index = sharks.index.str.capitalize()
    pie = sharks.plot.pie(autopct="%.1f%%", textprops={'color': 'black', 'fontsize': 10, 'va': 'center'})
    
    plt.title('Shark species vs number of attacks')
    # Save the plot as an image and display the plot
    plt.savefig('figures/species_vs_attacks_pie.png')
    os.system("start figures/species_vs_attacks_pie.png")
    plt.show()

def species_vs_attacks_fatality(df):
    """This function Creates a histplot with species column, Sum the counts of all species that attacked people and if the result
    was a fatality or not.
    args:
    -df: pandas DataFrame containing the shark attack data
    returns:
    -None
    """
    
    df_filtered1 = df.query('fatality in ["yes", "no"]')
    sns.histplot(data=df_filtered1, x="species", hue="fatality", multiple="stack");
    plt.xticks(rotation=90);
    plt.title('Shark species vs number of attacks and fatality')
    plt.xlabel('shark species')
    plt.ylabel('attacks');
    
    # Save the plot as an image and display the plot
    plt.savefig('figures/species_vs_attacks_fatality.png')
    os.system("start figures/species_vs_attacks_fatality.png")
    plt.show()


def fatality_sex(df):
    """This function Creates a histplot with the sum of all the attacked people, their sex and if the result was a fatality or not.
    args:
    -df: pandas DataFrame containing the shark attack data
    returns:
    -None
    """
    
    #Filter the data to include only "yes" or "no" in the "fatality" column and "m" or "f" in the "sex" column"
    df_filtered = df.query('fatality in ["yes", "no"] and sex in ["m", "f"] and fatality != "unknown"')
    #create the plot
    sns.histplot(data=df_filtered, x="sex", hue="fatality", multiple="stack")
    plt.title('Fatality vs Attacked person sex')
    plt.xlabel('Sex')
    plt.ylabel('Shark attacks');
    
    # Save the plot as an image and display the plot
    plt.savefig('figures/fatality_sex.png')
    os.system("start figures/fatality_sex.png")
    plt.show()

def species_vs_fatality(df):
    """This function Creates a histplot with species column, Sum the counts of all species that attacked people with a fatal result.
    args:
    -df: pandas DataFrame containing the shark attack data
    returns:
    -None
    """
    df_filter = df.query('fatality in "yes"')
    sns.histplot(data=df_filter, x="species", hue="fatality", multiple="stack");
    plt.xticks(rotation=90);
    plt.title('Shark species vs number of fatalities')
    plt.xlabel('shark species')
    plt.ylabel('Fatal attacks');
    
    # Save the plot as an image and display the plot
    plt.savefig('figures/species_vs_fatality.png')
    os.system("start figures/species_vs_fatality.png")
    plt.show()