"""Read and write the CSV files in data/processed and data/interim.

The table is wrapped in `#data-begin#` and `#data-end#` lines and dates are
stored as YYYYMM.
"""

import os

import pandas as pd


def write_marked_csv(df, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    if df.index.name == "Date":
        df = df.reset_index()
    if "Date" in df.columns and pd.api.types.is_datetime64_any_dtype(df["Date"]):
        df = df.assign(Date=df["Date"].dt.strftime("%Y%m"))
    with open(output_path, "w") as f:
        f.write("#data-begin#\n")
        df.to_csv(f, index=False)
        f.write("#data-end#\n")


def read_marked_csv(path):
    df = pd.read_csv(path, comment="#")
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"].astype(str), format="%Y%m")
    return df
