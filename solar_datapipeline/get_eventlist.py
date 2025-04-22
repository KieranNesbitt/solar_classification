import pandas as pd
import os
from manipulate_dataframe import time_code_to_bins
#import manipulate_dataframe 
headers: list[str] = ("Date","Time","Type","Stations")
base_url: str = "https://soleil.i4ds.ch/solarradio/data/BurstLists/2010-yyyy_Monstein/"
import numpy as np
years: list[int] = [2023,2024]
months: list[int] = list(range(1,13))

def get_txt(url: str, save_folder: str) -> None:
    """
    Request event list .txt file from e-callisto database \n

    url \n
        URL in string form, either given by user or generated from generate_urls function \n
    save_folder \n
        Base Directory that will is used to save the files

    """
    try:
        text_file: str = url.split("/")[-1]
        get_year: str = text_file.split("_")[1]
        print(f"Downloading event list: {text_file}")
        df = pd.read_table(url, comment= "#", names= headers, sep='\t', on_bad_lines='skip', encoding="ISO-8859-1").dropna() 
        #Explantion of the above code
        ##The data is tabular, with comments declared using "#" however some don't and so show up as rows with NaN in rows hence I drop any rows with NaN
        df["Time_code"] = df["Time"].apply(time_code_to_bins)
        save_folder = os.path.join(save_folder, get_year)
        if not os.path.exists(save_folder):
            #Here just incase directory is not set up
            os.makedirs(save_folder)
            print(f"{save_folder} created")
        save_path: str = os.path.join(save_folder, text_file)
        df.to_csv(save_path)
    except Exception as e:
        print(f"Error: {e}")

def get_multiple_txt(save_folder: str, years: list[int], months: list[int], base_url: str) -> None:
    """
    
    
    """
    for url in generate_urls(years, months, base_url):
        try:
            get_txt(url, save_folder)
        except Exception as e:
            print(f"Error downloading {url}: {e}")

def generate_urls(years: list[int], months: list[int], base_url: str):
    """
    Used to generate urls given the years and the months desired \n

    years\n
        List of years wanted
    Months\n
        List of months wanted
    base_url\n
        Used as the foundation to build the urls
    """
    for year in years:
        for month in months:
            yield f"{base_url}{year}/e-CALLISTO_{year}_{month:02d}.txt"
if __name__ == "__main__":
    save_folder: str = f"{os.getcwd()}\solar_data_folder\events_list"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    get_multiple_txt(save_folder, years, months, base_url)