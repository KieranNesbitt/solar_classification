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


def create_start_time_column(df: pd.DataFrame) -> None:
    start_and_end: pd.Series = df["Time"]
    start_and_end_split: pd.Series[list[int]]  = start_and_end.str.split("-")
    list_swap: pd.Series[list[int]] = start_and_end_split[df["Type"] == "CTM"]
    
    time_binning(start_and_end_split.head(10))

def time_binning(time_series: pd.Series, bin_interval: int = 15):

    print(time_series)
    
def create_time_bins_optimized(step_minutes=15) -> list[int]:
    """
    Creates time bins from 0000 to 2345 in specified minute steps (optimized).

    Args:
        step_minutes (int): The step size in minutes for the time bins.
                           Must be a divisor of 60.

    Returns:
        list: A list of strings representing the time bins in HHMM format.
    """
    if 60 % step_minutes != 0:
        raise ValueError("Step minutes must be a divisor of 60.")

    num_steps_per_hour = 60 // step_minutes
    total_steps = 24 * num_steps_per_hour
    time_bins = []

    for i in range(total_steps+1):
        minutes = (i * step_minutes) % 60
        hours = (i * step_minutes) // 60
        time_str = "{:02d}{:02d}".format(hours, minutes)
        time_bins.append(time_str)

    return time_bins

# Create time bins in 15-minute steps
fifteen_minute_bins = create_time_bins_optimized(step_minutes=15)
print(fifteen_minute_bins)