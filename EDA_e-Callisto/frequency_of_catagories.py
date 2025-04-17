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
    fig, ax = plt.subplots(1,2)
    sns.barplot(ax=ax[0], data=df_confirmed_type, x="Type", y = "Stations")
    sns.barplot(ax=ax[1], data=df_unconfirmed_type, x="Type", y = "Stations")

    ax[0].bar_label(ax[0].containers[0], fontsize=10)
    ax[0].set_title("Confirmed Observations for 2024")
    ax[0].set_ylabel("Total Observations")
    ax[0].grid()

    ax[1].bar_label(ax[1].containers[0], fontsize=10)
    ax[1].set_title("Unconfirmed Observations for 2024")
    ax[1].set_ylabel("Total Observations")
    ax[1].grid()
    
    sns.despine(trim=True)
    plt.xticks(rotation=90)
    plt.show()


