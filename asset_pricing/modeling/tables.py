"""Write result tables to reports/tables; shared by both modeling stages."""

import pandas as pd


def add_average_row(df):
    """Append a row named "Average" with the mean of every numeric column."""
    avg = {df.columns[0]: "Average"}
    for col in df.select_dtypes(include=["number"]).columns:
        avg[col] = df[col].mean()
    return pd.concat([df, pd.DataFrame([avg])], ignore_index=True)


def write_table(df, path, index=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=index)
