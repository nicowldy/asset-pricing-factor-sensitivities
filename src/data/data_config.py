"""Data configuration bridge importing from central src.config."""
from pathlib import Path
try:
    from src.config import (
        PROJECT_ROOT,
        DATA_DIR,
        RAW_DIR as RAW_DIR_PATH,
        PROCESSED_DIR as PROCESSED_DIR_PATH,
        REPORTS_DIR,
        TABLES_DIR,
        PROCESSING_STATS as PROCESSING,
        DATA_DATE,
        FF_CAPM_RAW,
        FF_FF3_RAW,
        FF_FF5_RAW,
        FF_IND_RAW,
        FF_CAPM_PROCESSED,
        FF_FF3_PROCESSED,
        FF_FF5_PROCESSED,
        FF_IND_PROCESSED,
        get_standard_datasets,
    )
except ModuleNotFoundError:
    import os
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
    DATA_DIR = os.path.join(PROJECT_ROOT, "data")
    RAW_DIR_PATH = os.path.join(DATA_DIR, "raw")
    PROCESSED_DIR_PATH = os.path.join(DATA_DIR, "processed")
    REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
    TABLES_DIR = os.path.join(REPORTS_DIR, "tables")
    PROCESSING = os.path.join(TABLES_DIR, "data_sample.csv")
    DATA_DATE = "2025-02-24"
    FF_CAPM_RAW = os.path.join(RAW_DIR_PATH, f"ff_capm_monthly_pct_raw_{DATA_DATE}.csv")
    FF_FF3_RAW = os.path.join(RAW_DIR_PATH, f"ff_ff3_monthly_pct_raw_{DATA_DATE}.csv")
    FF_FF5_RAW = os.path.join(RAW_DIR_PATH, f"ff_ff5_monthly_pct_raw_{DATA_DATE}.csv")
    FF_IND_RAW = os.path.join(RAW_DIR_PATH, f"ff_ind_monthly_pct_raw_{DATA_DATE}.csv")
    FF_CAPM_PROCESSED = os.path.join(PROCESSED_DIR_PATH, "ff_capm_processed.csv")
    FF_FF3_PROCESSED = os.path.join(PROCESSED_DIR_PATH, "ff_ff3_processed.csv")
    FF_FF5_PROCESSED = os.path.join(PROCESSED_DIR_PATH, "ff_ff5_processed.csv")
    FF_IND_PROCESSED = os.path.join(PROCESSED_DIR_PATH, "ff_ind_processed.csv")

    def get_standard_datasets():
        return [
            {"input": FF_CAPM_RAW, "output": FF_CAPM_PROCESSED, "name": "capm"},
            {"input": FF_FF3_RAW, "output": FF_FF3_PROCESSED, "name": "ff3"},
            {"input": FF_FF5_RAW, "output": FF_FF5_PROCESSED, "name": "ff5"},
            {"input": FF_IND_RAW, "output": FF_IND_PROCESSED, "name": "ind"},
        ]
