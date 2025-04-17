import numpy as np
import pandas as pd 
import os 
import glob
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_context("paper")
sns.set_style("ticks")

if __name__ == "__main__":
    cat = ("CTM", "II", "III", "IV", "V", "U", "J","VI","VII")
    path = r"C:\Users\kwnes\Documents\solar_classification\solar_data_folder\events_list\2024"
    file_paths = os.path.join(path, "*.txt")
    df = pd.concat(map(pd.read_csv, glob.glob(file_paths)))
    df_grouped_type = pd.DataFrame(df.groupby("Type").count()['Stations'].sort_values(ascending=False))
    df_confirmed_type = df_grouped_type.loc[df_grouped_type.index.isin(cat)]
    df_unconfirmed_type = df_grouped_type[df_grouped_type.index.str.contains("\?")]
    ax = plt.figure(layout="constrained").subplot_mosaic(
    """
    AA
    BC
    """
)
    sns.barplot(ax=ax["A"], data=df_grouped_type, x="Type", y = "Stations")
    sns.barplot(ax=ax["B"], data=df_confirmed_type, x="Type", y = "Stations")
    sns.barplot(ax=ax["C"], data=df_unconfirmed_type, x="Type", y = "Stations")
    ax["A"].bar_label(ax["A"].containers[0], fontsize=10)
    ax["A"].set_title("Observations for 2024")
    ax["A"].set_ylabel("Total Observations")
    ax["A"].grid()

    ax["B"].bar_label(ax["B"].containers[0], fontsize=10)
    ax["B"].set_title("Confirmed Observations for 2024")
    ax["B"].set_ylabel("Total Observations")
    ax["B"].grid()

    ax["C"].bar_label(ax["C"].containers[0], fontsize=10)
    ax["C"].set_title("Unconfirmed Observations for 2024")
    ax["C"].set_ylabel("Total Observations")
    ax["C"].grid()
    
    sns.despine(trim=True)
    plt.xticks(rotation=90)
    plt.show()


