import pandas as pd
import os
import numpy as np

def playing_with_df(df: pd.DataFrame) -> None:
    start_and_end = df["Time"]
    start_and_end_split = start_and_end.str.split("-")
    list_swap: list[list[int]] = start_and_end_split[df["Type"] == "CTM"].to_list()
    print(pd.Series((v for v in list_swap)).set_axis(start_and_end_split[df["Type"] == "CTM"].index.to_list()))
    print("")
    print(start_and_end_split[df["Type"] == "CTM"].index.to_list())


def mapper_function_converter(time_code: list[str]) -> list[int]:
    try:
         return int(time_code)
    except:
        return 0

def time_code_to_bins(time_code: str) -> list[str]: #     Needed when using the events list to act like a look up table to grab the specific data for the radio burst type

    """
    Converts a 'HH:MM-HH:MM' time code to a list of 15-minute bins in 'HHMM00' format.
    Needed when using the events list to act like a look up table to grab the specific data for the radio burst type
    Args:
        time_code (str): The time code string (e.g., "15:58-16:23").

    Returns:
        list: A list of 'HHMM00' strings representing the 15-minute bins.
    """
    #Weird anomalies such as . instead of : need to removed, using translate and a dictionary should help
    replacement_dict = {".":":", ";":":", "+":"", "_": ":"}
    replacements = str.maketrans(replacement_dict)
    time_code= time_code.translate(replacements)
    if time_code.count(":")>2:
        return []
    start_time_str, end_time_str = time_code.split('-')

    start_hours, start_minutes = map(mapper_function_converter, start_time_str.split(':'))
    end_hours, end_minutes = map(mapper_function_converter, end_time_str.split(':'))

    start_total_minutes = (start_hours * 60) + start_minutes
    end_total_minutes = (end_hours * 60) + end_minutes

    start_bin_minute = (start_total_minutes // 15) * 15
    end_bin_minute = (end_total_minutes // 15) * 15

    bins = []
    current_bin_minute = start_bin_minute
    while current_bin_minute <= end_bin_minute:
        bin_hours = current_bin_minute // 60
        bin_minutes = current_bin_minute % 60
        bins.append(f"{bin_hours:02d}{bin_minutes:02d}00")
        current_bin_minute += 15
    return bins
#Test code
"""single_time_code = "00.01.00:01"
bin_results = time_code_to_bins(single_time_code)
print(f"Time code '{single_time_code}' falls into bins '{bin_results}'")"""