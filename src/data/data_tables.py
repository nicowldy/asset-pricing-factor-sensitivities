"""Export preprocessing metrics and sample summaries to CSV."""
from __future__ import annotations

import os
from pathlib import Path
import pandas as pd


def export_processing_statistics(statistics: dict, stats_filepath: str | Path) -> None:
    headers = [
        "name",
        "raw_rows",
        "processed_rows",
        "raw_range",
        "processed_range",
        "dropped_cleaning",
        "dropped_intersection",
    ]
    df = pd.DataFrame(statistics["datasets"].values())
    for col in headers:
        if col not in df.columns:
            df[col] = None
    os.makedirs(os.path.dirname(str(stats_filepath)), exist_ok=True)
    df[headers].to_csv(stats_filepath, index=False)
