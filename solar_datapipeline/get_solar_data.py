import requests
import os
import pandas as pd
from functools import wraps
from time import time

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r args:[%r, %r] took: %2.5f sec' % \
          (f.__name__, args, kw, te-ts))
        return result
    return wrap

def convert_stations(stations: str) -> list[str]:
    """
    Converts the stations string to a list of station names.
    """
    # Split the string by commas and strip whitespace
    return [station.strip() for station in stations.split(",")]

def download_multiple_files(urls:str, save_path:str) -> None:
    for url in urls:
        try:
            file_name: str = url.split("/")[-1]
            save_path:str = os.path.join(save_path, file_name)
            download_file(url, save_path)
        except Exception as e:
            print(f"Error downloading {url}: {e}")

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

def get_event_list(year: int, month: int, cwd: str) -> pd.DataFrame:
    """
    Gets the event list based on the year and month provided.
    """
    file_path: str = os.path.join(cwd, "solar_data_folder", "events_list", str(year), f"e-CALLISTO_{year}_{month:02d}.txt")

    try:
        df: pd.DataFrame = pd.read_csv(file_path, comment="#", sep=',', on_bad_lines='skip', encoding="ISO-8859-1",
                         usecols=['Date', 'Type', "Stations", "Time_code"], converters={'Time_code': pd.eval, "Stations": convert_stations})
        return df
    except Exception as e:
        print(f"Error fetching event list: {e}")

        return pd.DataFrame()


#Example URL: "https://soleil.i4ds.ch/solarradio/qkl/2024/08/04/EGYPT-SpaceAgency_20240804_121501_01.fit.gz.png"
def create_function_urls(date_code: int, stations: list[str]) -> list[str]:
    """
    Generates base URLs for the given year and month.
    """
    #date_code: "YYYYMMDD" format
    year, month, day = date_code // 10000, (date_code // 100) % 100, date_code % 100
    urls: list[str] = []
    for station in stations:
        if "(" in station or "[" in station or "?" in station:
            continue
        url: str = f"https://soleil.i4ds.ch/solarradio/qkl/{year}/{month:02d}/{day:02d}/{station}_{year}{month:02d}{day:02d}"
        urls.append(url)
    #Unfortunately, the URL format is not consistent, as the time code does always match the every 15 minute interval, varing by a couple minutes/seconds
    #So the url will be generated for the whole day, and the user will have to check the time code manually through a loop
    return urls

def generate_timecode_urls(timecodes: str, url: str):
    
    pass


@timing
def main() -> None:
    cwd: str = os.getcwd()
    base_url: str = "https://soleil.i4ds.ch/solarradio/qkl/" # "http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto"
    year: int = 2024
    month:int = 1
    if os.path.exists(f"{cwd}\solar_data_folder"):
       df = get_event_list(year, month, cwd)
       for index, row in df.iterrows():
            
            print(create_function_urls(row["Date"], row["Stations"]))
            
    else:
        os.makedirs(f"{cwd}\solar_data_folder\solar_data")
        print(f"{cwd}\solar_data_folder\solar_data created")
if __name__ == "__main__":
    main()

    
    