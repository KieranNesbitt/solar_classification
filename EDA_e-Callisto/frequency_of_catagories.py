import numpy as np
import pandas as pd 
import os 
import glob
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_context("paper")
sns.set_style("ticks")

if __name__ == "__main__":
    path = r"C:\Users\kwnes\Documents\solar_classification\solar_data_folder\events_list\2024"
    file_paths = os.path.join(path, "*.txt")
    df = pd.concat(map(pd.read_csv, glob.glob(file_paths)))
    df_grouped_type = pd.DataFrame(df.groupby("Type").count()['Stations'].sort_values(ascending=False))

    df_confirmed_type = df_grouped_type.drop(index=("REM"))
    fig = plt.figure()
    ax = sns.barplot(df_confirmed_type, x="Type", y = "Stations")
    ax.bar_label(ax.containers[0], fontsize=10)
    ax.set_title("Observations for 2024")
    ax.set_ylabel("Total Observations")
    ax.set_xlabel("Radio Burst Classification")
    fig.autofmt_xdate(rotation=45)

    sns.despine(trim=True)
    plt.grid()
    plt.show()


