import pandas as pd


def load_data_with_markers(path):
    try:
        df = pd.read_csv(path, comment="#")
    except (FileNotFoundError, IOError):
        return pd.DataFrame()
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], format="%Y%m")
    return df


def get_industry_names(df):
    return [c for c in df.columns if c != "Date"]
