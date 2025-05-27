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

def get_event_list(year: int, month: int, cwd: str, Type: None) -> pd.DataFrame:
    """
    Gets the event list based on the year and month provided.
    """
    file_path: str = os.path.join(cwd, "solar_data_folder", "events_list", str(year), f"e-CALLISTO_{year}_{month:02d}.txt")

    try:
        df: pd.DataFrame = pd.read_csv(file_path, comment="#", sep=',', on_bad_lines='skip', encoding="ISO-8859-1",
                         usecols=['Date', 'Type', "Stations", "Time_code"], converters={'Time_code': pd.eval, "Stations": convert_stations})
        if Type is not None:
            return df[df["Type"] == Type]
        return df
    except Exception as e:
        print(f"Error fetching event list: {e}")

        return pd.DataFrame()
@timing
def main(year: int = 2024, month: int = 1, Type: str = None):
    output_dir = os.path.join(cwd, "solar_data_folder")
    output_file_path = os.path.join(output_dir, "solar_data_url.txt") # Using .txt for plain text
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Directory '{output_dir}' created.")
    
    events_list = get_event_list(year, month, cwd, Type)

    # Open the file in write mode ('w') to overwrite existing content or create a new file
    # If you want to append to the file, change 'w' to 'a'.
    url_full = []
    with open(output_file_path, 'w') as f:
        print(f"Saving URLs to '{output_file_path}'...")
        for index, row in events_list.iterrows():
            # Ensure 'Stations' and 'Time_code' are treated as lists
            stations_list = row["Stations"] if isinstance(row["Stations"], list) else [row["Stations"]]
            time_codes_list = row["Time_code"] if isinstance(row["Time_code"], list) else [row["Time_code"]]

            urls_generator = generate_all_image_urls(
                row["Date"],
                stations_list,
                time_codes_list,
                2,
                base_url 
            )
            
            # Iterate directly over the generator and write each URL to the file
            for url in urls_generator:
                url_full.append(url)
        url_df = pd.DataFrame(url_full)
        url_df.to_csv(output_file_path, index=False, header=None)

if __name__ == "__main__":
    from create_solardata_url import generate_all_image_urls
    cwd: str = os.getcwd()
    base_url: str = "https://soleil.i4ds.ch/solarradio/qkl/" # "http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto"
    lookup_dic: pd.DataFrame = pd.read_csv(fr"{cwd}\solar_datapipeline\focuscode_lookup.csv", sep = ",", header=0)
    main(Type = "II")

    
    