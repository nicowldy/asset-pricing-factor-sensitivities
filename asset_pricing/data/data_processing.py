import pandas as pd

from asset_pricing.config import PROCESSING_STATS, get_standard_datasets
from asset_pricing.data.data_tables import export_processing_statistics
from asset_pricing.data.data_utils import save_with_markers


def _date_range(dates) -> str:
    return f"{dates.min():%Y%m} to {dates.max():%Y%m}"


def process_data():
    stats, dfs = {}, []
    for ds in get_standard_datasets():
        raw = pd.read_csv(ds["input"])
        raw.columns = ["Date", *raw.columns[1:]]
        if "columns" in ds:
            raw = raw[["Date", *ds["columns"]]]
        raw_dates = pd.to_datetime(raw["Date"], format="%Y%m")
        df = raw.replace([-99.99, -999], pd.NA).dropna()
        df["Date"] = pd.to_datetime(df["Date"], format="%Y%m")
        name = ds["name"]
        stats[name] = {
            "name": name,
            "raw_rows": len(raw),
            "raw_range": _date_range(raw_dates),
            "dropped_cleaning": len(raw) - len(df),
        }
        dfs.append((name, df.set_index("Date"), ds["output"]))

    common_idx = dfs[0][1].index
    for _, df, _ in dfs[1:]:
        common_idx = common_idx.intersection(df.index)

    for name, df, output in dfs:
        df_proc = df.loc[common_idx]
        stats[name].update(
            processed_rows=len(df_proc),
            processed_range=_date_range(common_idx),
            dropped_intersection=len(df) - len(df_proc),
        )
        save_with_markers(df_proc, output)

    export_processing_statistics({"datasets": stats}, PROCESSING_STATS)


if __name__ == "__main__":
    process_data()
