import numpy as np
import pandas as pd 
import os 
import glob
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_context("paper")
sns.set_style("ticks")

if __name__ == "__main__":
    year = 2023
    cat = ("CTM", "II", "III", "IV", "V","VI","VII", "U", "J")
    path = rf"{os.getcwd()}\solar_data_folder\events_list\{year}"
    file_paths = os.path.join(path, "*.txt")
    df = pd.concat(map(pd.read_csv, glob.glob(file_paths)))
    df_grouped_type = pd.DataFrame(df.groupby("Type").count()['Stations'].sort_values(ascending=False))
    df_confirmed_type = df_grouped_type.loc[df_grouped_type.index.isin(cat)]
    df_unconfirmed_type = df_grouped_type[df_grouped_type.index.str.contains("\?")]
    df_other_type = df_grouped_type[~df_grouped_type.index.str.contains("\?") & ~df_grouped_type.index.isin(cat)]
    ax = plt.figure(layout="constrained").subplot_mosaic(
    """
    AA
    BC
    """
)   
    sns.barplot(ax=ax["A"], data=df_confirmed_type, x=df_confirmed_type.index, y = "Stations")
    sns.barplot(ax=ax["B"], data=df_unconfirmed_type, x=df_unconfirmed_type.index, y = "Stations")
    sns.barplot(ax=ax["C"], data=df_other_type, x=df_other_type.index , y = "Stations")
    ax["A"].bar_label(ax["A"].containers[0], fontsize=10)
    ax["A"].set_title(f"Confirmed Observations for {year}")
    ax["A"].set_ylabel("Total Observations")
    ax["A"].grid()

    ax["B"].bar_label(ax["B"].containers[0], fontsize=10)
    ax["B"].set_title(f"Unconfirmed Observations for {year}")
    ax["B"].set_ylabel("Total Observations")
    ax["B"].grid()

    ax["C"].bar_label(ax["C"].containers[0], fontsize=10)
    ax["C"].set_title("'Other' categories")
    ax["C"].set_ylabel("Total Observations")
    ax["C"].grid()
    
    sns.despine(trim=True)
    plt.xticks(rotation=90)
    plt.show()


