import pandas as pd
import os
headers = ("Date","Time","Type","Stations")
def get_txt(url: str, save_folder: str):
    try:
        text_file = url.split("/")[-1]
        print(f"Downloading event list: {text_file}")
        df = pd.read_table(url, comment= "#", names= headers, sep='\t', on_bad_lines='skip').dropna()
        save_path = os.path.join(save_folder, text_file)
        df.to_csv(save_path)
    except Exception as e:
        print(f"Error: {e}")

def get_multiple_txt(urls:list, save_folder: str):
    pass
save_folder: str = f"{os.getcwd()}\solar_data_folder\events_list"
test_url: str = "https://soleil.i4ds.ch/solarradio/data/BurstLists/2010-yyyy_Monstein/2024/e-CALLISTO_2024_03.txt"
get_txt(test_url, save_folder)