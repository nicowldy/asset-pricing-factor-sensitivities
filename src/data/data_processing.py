import pandas as pd
try:
    from src.config import PROCESSING_STATS, get_standard_datasets
    from src.data.data_utils import save_with_markers
    from src.data.data_tables import export_processing_statistics
except ModuleNotFoundError:
    from data_config import PROCESSING as PROCESSING_STATS, get_standard_datasets
    from data_utils import save_with_markers
    from data_tables import export_processing_statistics


def process_data():
    stats, dfs = {}, []
    for ds in get_standard_datasets():
        input_path = str(ds["input"])
        output_path = str(ds["output"])
        df = pd.read_csv(input_path)
        df.columns = ["Date"] + list(df.columns[1:])
        df = df.replace([-99.99, -999], pd.NA).dropna()
        df["Date"] = pd.to_datetime(df["Date"], format="%Y%m")
        idx = df["Date"]
        name = ds["name"]
        stats[name] = {
            "name": name,
            "raw_rows": len(df),
            "raw_range": f"{idx.iloc[0].strftime('%Y%m')} to {idx.iloc[-1].strftime('%Y%m')}",
            "cleaned_rows": len(df),
            "cleaned_range": f"{idx.iloc[0].strftime('%Y%m')} to {idx.iloc[-1].strftime('%Y%m')}",
        }
        dfs.append((name, df.set_index("Date"), output_path))

    common_idx = dfs[0][1].index
    for _, df, _ in dfs[1:]:
        common_idx = common_idx.intersection(df.index)

    for name, df, output in dfs:
        df_proc = df.loc[common_idx]
        st = stats[name]
        st.update(
            {
                "processed_rows": len(df_proc),
                "processed_range": f"{common_idx.min().strftime('%Y%m')} to {common_idx.max().strftime('%Y%m')}",
                "dropped_cleaning": st["raw_rows"] - st["cleaned_rows"],
                "dropped_intersection": st["cleaned_rows"] - len(df_proc),
            }
        )
        save_with_markers(df_proc, output)

    export_processing_statistics({"datasets": stats}, str(PROCESSING_STATS))


if __name__ == "__main__":
    process_data()
