import pandas as pd
import requests
import os

def generate_timecode_urls(middle_url: str, timecodes_iterable, station_name: str, timeout: int = 5):
    cwd: str = os.getcwd()
    lookup_dic: pd.DataFrame = pd.read_csv(fr"{cwd}\solar_datapipeline\focuscode_lookup.csv", sep = ",", header=0)
    station_row = lookup_dic.loc[lookup_dic["Station Name"] == station_name]
    
    if station_row.empty:
        print(f"Warning: Station '{station_name}' not found in lookup_dic. No URLs will be generated.")
        return 

    focus_codes: list[str] = station_row["Two-Digit-Code"].to_list()
    
    if not focus_codes:
        print(f"Warning: No 'Two-Digit-Code' found for station '{station_name}'. No URLs will be generated.")
        return 

    timecodes_list = list(timecodes_iterable) 

    for focus in focus_codes:
        for timecode in timecodes_list:
            url_final: str = f"{middle_url}_{timecode}_{focus}.fit.gz.png"
            try:
                response = requests.head(url_final, timeout=timeout)
                if 200 <= response.status_code < 300:
                    yield url_final
                    break
                else:
                    pass

            except requests.exceptions.RequestException as e:
                print(f"Error checking URL {url_final}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred for {url_final}: {e}")
def generate_surrounding_timecodes_generator(center_timecode_str: str, surrounding_range: int):
    if not (isinstance(center_timecode_str, str) and len(center_timecode_str) == 6 and center_timecode_str.isdigit()):
        raise ValueError("Center timecode must be a 6-digit string (HHMMSS).")
    if not (isinstance(surrounding_range, int) and surrounding_range >= 0):
        raise ValueError("Surrounding range must be a non-negative integer.")

    hours = int(center_timecode_str[0:2])
    minutes = int(center_timecode_str[2:4])
    seconds = int(center_timecode_str[4:6])

    if not (0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60):
        raise ValueError("Invalid time components in the central timecode.")

    center_total_seconds = (hours * 3600) + (minutes * 60) + seconds
    
    SECONDS_IN_DAY = 24 * 3600

    yield center_timecode_str 

    other_timecodes_set = set() 

    for offset in range(-surrounding_range, surrounding_range + 1):
        if offset == 0: 
            continue

        current_total_seconds = center_total_seconds + offset
        
        normalized_total_seconds = (current_total_seconds % SECONDS_IN_DAY + SECONDS_IN_DAY) % SECONDS_IN_DAY

        h = normalized_total_seconds // 3600
        remaining_s = normalized_total_seconds % 3600
        m = remaining_s // 60
        s = normalized_total_seconds % 60

        formatted_timecode = "{:02d}{:02d}{:02d}".format(h, m, s)
        other_timecodes_set.add(formatted_timecode)
    
    for tc in sorted(list(other_timecodes_set)):
        yield tc

def generate_all_image_urls(date_code: int, stations: list[str], center_timecodes: list[str], surrounding_range: int, base_url: str):
    """
    Generates all possible image URLs as a generator for multiple center timecodes.

    Args:
        date_code (int): Date in YYYYMMDD format.
        stations (list[str]): List of station names.
        center_timecodes (list[str]): A list of central timecode strings.
        surrounding_range (int): The range +/- from each central timecode.

    Yields:
        str: A generated image URL that exists.
    """
    year, month, day = date_code // 10000, (date_code // 100) % 100, date_code % 100

    for station in stations:
        if "(" in station or "[" in station or "?" in station:
            continue
        
        middle_url: str = f"{base_url}{year}/{month:02d}/{day:02d}/{station}_{year}{month:02d}{day:02d}"
        
        # Iterate through each center timecode provided
        for single_center_timecode in center_timecodes:
            # Create a new timecode generator for each unique center timecode
            timecode_gen = generate_surrounding_timecodes_generator(single_center_timecode, surrounding_range)
            
            # Now, use this timecode generator to get URLs for the current station and timecode group
            for final_url in generate_timecode_urls(middle_url, timecode_gen, station):
                yield final_url

"""def main():
    # --- Example Usage ---
    date_code_example = 20240131
    stations_example = ["Australia-ASSA"] 
    # Now a list of center timecodes
    center_timecodes = ["051500"]
    range_around = 2

    # Call generate_all_image_urls with the list of center timecodes
    final_url_generator = generate_all_image_urls(
        date_code_example, 
        stations_example, 
        center_timecodes, # Pass the list here
        range_around
    )

    print("Generated URLs (from pipeline with multiple centers):")
    for url in final_url_generator:
        print(url)

if __name__ == "__main__":
    cwd: str = os.getcwd()
    base_url = "https://soleil.i4ds.ch/solarradio/qkl/"
    lookup_dic: pd.DataFrame = pd.read_csv(fr"{cwd}\solar_datapipeline\focuscode_lookup.csv", sep = ",", header=0)

    main()"""