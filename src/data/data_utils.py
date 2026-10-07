import os
import pandas as pd


def save_with_markers(df, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = df.copy()
    if "Date" not in df.columns:
        df = df.reset_index().rename(columns={"index": "Date"})
    if pd.api.types.is_datetime64_any_dtype(df["Date"]):
        df["Date"] = df["Date"].dt.strftime("%Y%m")
    with open(output_path, "w") as f:
        f.write("#data-begin#\n")
        df.to_csv(f, index=False)
        f.write("#data-end#\n")


def load_data_with_markers(path):
    try:
        df = pd.read_csv(path, comment="#")
    except (FileNotFoundError, IOError):
        return pd.DataFrame()
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"].astype(str), format="%Y%m")
    return df
