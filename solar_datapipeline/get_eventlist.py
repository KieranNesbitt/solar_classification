import pandas as pd
import os
headers = ("Date","Time","Type","Stations")
def get_txt(url, save_folder):
    try:
        print("Downloading")
        df = pd.read_table(url, comment= "#", names= headers).dropna()
        start_date = df["Date"][0]
        end_date = df["Date"][1]
        save_path = os.path.join(save_folder, f"{start_date}_{end_date}")
        df.to_csv(save_path)
    
    except Exception as e:
        print(f"Error: {e}")

save_folder = f"{os.getcwd()}\solar_data_folder\events_list"
test_url = "https://soleil.i4ds.ch/solarradio/data/BurstLists/2010-yyyy_Monstein/2024/e-CALLISTO_2024_01.txt"
get_txt(test_url, save_folder)