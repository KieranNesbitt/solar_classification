import requests
import os
import pandas as pd

def download_file(url, save_path):
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


def download_multiple_files(urls, save_path):
    for url in urls:
        try:
            file_name = url.split("/")[-1]
            save_path = os.path.join(save_path, file_name)
            download_file(url, save_path)
        except Exception as e:
            print(f"Error downloading {url}: {e}")
def url_generator(dataframe, Types):
    pass

if __name__ == "__main__":
    cwd = os.getcwd()
    test_url = "http://soleil80.cs.technik.fhnw.ch/solarradio/data/2002-20yy_Callisto/2025/02/01/ALASKA-ANCHORAGE_20250201_000000_01.fit.gz"
    if os.path.exists(f"{cwd}\solar_data_folder"):
        save_path = os.path.join(f"{cwd}\solar_data_folder", "ALASKA-ANCHORAGE_20250201.fit.gz")
        download_file(test_url, save_path )
    else:
        os.makedirs(f"{cwd}\solar_data_folder")

    
    