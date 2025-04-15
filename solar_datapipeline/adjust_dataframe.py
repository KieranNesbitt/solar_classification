import pandas as pd
import os

def create_start_time_column(df: pd.DataFrame):
    start_and_end = df["Time"]
    start_and_end_split = start_and_end.str.split("-")
    print(start_and_end_split[df["Type"] == "RSP"])