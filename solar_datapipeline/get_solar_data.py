import requests
import os
import pandas as pd

def download_file(url: str, save_path: str):
    try:

        response = requests.get(url)  
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"File downloaded successfully: {save_path}")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

"https://soleil.i4ds.ch/solarradio/qkl/2024/08/04/EGYPT-SpaceAgency_20240804_121501_01.fit.gz.png"

def get_event_list(year: int, month: int, cwd: str) -> pd.DataFrame:
    """
    Gets the event list based on the year and month provided.
    """
    file_path: str = os.path.join(cwd, "solar_data_folder", "events_list", str(year), f"e-CALLISTO_{year}_{month:02d}.txt")

    try:
        df: pd.DataFrame = pd.read_csv(file_path, comment="#", sep=',', on_bad_lines='skip', encoding="ISO-8859-1",
                         usecols=['Date', 'Type', "Stations", "Time_code"], converters={'Time_code': pd.eval})
        print(df[df["Type"]== "CTM"]["Time_code"])
        return df
    except Exception as e:
        print(f"Error fetching event list: {e}")

        return pd.DataFrame()

def download_multiple_files(urls:str, save_path:str) -> None:
    for url in urls:
        try:
            file_name: str = url.split("/")[-1]
            save_path:str = os.path.join(save_path, file_name)
            download_file(url, save_path)
        except Exception as e:
            print(f"Error downloading {url}: {e}")
def generate_urls(date_code: int, stations: str, time_code: str) -> list[str]:
    """
    Generates URLs for the given year and month.
    """
    #date_code: "YYYYMMDD" format
    year, month, day = date_code // 10000, (date_code // 100) % 100, date_code % 100
    urls: list[str] = []

    
    return urls
if __name__ == "__main__":
    cwd: str = os.getcwd()
    base_url: str = "https://soleil.i4ds.ch/solarradio/qkl/" # "http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto"
    year: int = 2024
    month:int = 1
    if os.path.exists(f"{cwd}\solar_data_folder"):
       get_event_list(year, month, cwd)
       generate_urls(20241224, "EGYPT-SpaceAgency", "004500")
    else:
        os.makedirs(f"{cwd}\solar_data_folder\solar_data")
        print(f"{cwd}\solar_data_folder\solar_data created")

    
    