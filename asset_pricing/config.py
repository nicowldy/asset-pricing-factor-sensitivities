"""Centralized configuration and path management using pathlib."""

from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"

REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
TABLES_DIR = REPORTS_DIR / "tables"
OTHER_DIR = REPORTS_DIR / "other"

# Factor Models Configuration
MODELS = {
    "capm": {"factors": ["MKT"]},
    "ff3": {"factors": ["MKT", "SMB", "HML"]},
    "ff5": {"factors": ["MKT", "SMB", "HML", "RMW", "CMA"]},
}

DATA_DATE = "2025-02-24"

# Raw Data Paths
FF_FF3_RAW = RAW_DIR / f"ff_ff3_monthly_pct_raw_{DATA_DATE}.csv"
FF_FF5_RAW = RAW_DIR / f"ff_ff5_monthly_pct_raw_{DATA_DATE}.csv"
FF_IND_RAW = RAW_DIR / f"ff_ind_monthly_pct_raw_{DATA_DATE}.csv"

# Processed Data Paths
FF_CAPM_PROCESSED = PROCESSED_DIR / "ff_capm_processed.csv"
FF_FF3_PROCESSED = PROCESSED_DIR / "ff_ff3_processed.csv"
FF_FF5_PROCESSED = PROCESSED_DIR / "ff_ff5_processed.csv"
FF_IND_PROCESSED = PROCESSED_DIR / "ff_ind_processed.csv"
PROCESSED = {
    "capm": FF_CAPM_PROCESSED,
    "ff3": FF_FF3_PROCESSED,
    "ff5": FF_FF5_PROCESSED,
}

# Interim Data Paths
TRAINED = {m: INTERIM_DIR / f"ff_{m}_trained.csv" for m in MODELS}
TESTED = {m: INTERIM_DIR / f"ff_{m}_tested.csv" for m in MODELS}

# Reports - Tables
PROCESSING_STATS = TABLES_DIR / "data_sample.csv"
DESCRIPT_IND_TABLE = TABLES_DIR / "expl_descript_ind.csv"
ASSUMPTIONS_TABLE = TABLES_DIR / "expl_assumptions.csv"
INCRWALD_CAPM_TABLE = TABLES_DIR / "expl_incrwald_capm.csv"
INCRWALD_FF3_TABLE = TABLES_DIR / "expl_incrwald_ff3.csv"
PRED_METRICS_TABLE = TABLES_DIR / "pred_metrics.csv"
PRED_TTEST_TABLE = TABLES_DIR / "pred_ttest.csv"
PRED_PAIRTTEST_TABLE = TABLES_DIR / "pred_pairttest.csv"

# Reports - Figures
FIG_RSQ = FIGURES_DIR / "expl_rsq.svg"
FIG_DISTRIB_IND = FIGURES_DIR / "expl_distrib_ind.svg"
FIG_DISTRIB_FACT = FIGURES_DIR / "expl_distrib_fact.svg"
FIG_CUMRETURNS_FACT = FIGURES_DIR / "expl_cumreturns_fact.svg"
FIG_CUMRETURNS_IND = FIGURES_DIR / "expl_cumreturns_ind.svg"
FIG_RSQBYDECS = FIGURES_DIR / "expl_rsqbydecs.svg"
FIG_ALPHABYDECS = FIGURES_DIR / "expl_alphabydecs.svg"
FIG_PRED_RSQ = FIGURES_DIR / "pred_rsq.svg"
FIG_PRED_RMSE = FIGURES_DIR / "pred_rmse.svg"
FIG_PRED_COMPEXAM = FIGURES_DIR / "pred_compexample.svg"


def get_standard_datasets():
    return [
        # CAPM has no raw file of its own: MKT and RF come from the FF3 file.
        {
            "input": FF_FF3_RAW,
            "output": FF_CAPM_PROCESSED,
            "name": "capm",
            "columns": ["MKT", "RF"],
        },
        {"input": FF_FF3_RAW, "output": FF_FF3_PROCESSED, "name": "ff3"},
        {"input": FF_FF5_RAW, "output": FF_FF5_PROCESSED, "name": "ff5"},
        {"input": FF_IND_RAW, "output": FF_IND_PROCESSED, "name": "ind"},
    ]


def get_descript_model_path(model_name: str) -> Path:
    return TABLES_DIR / f"expl_descript_{model_name}.csv"


def get_jointwald_path(model_name: str) -> Path:
    return TABLES_DIR / f"expl_jointwald_{model_name}.csv"


def get_params_path(model_name: str) -> Path:
    return TABLES_DIR / f"expl_regress_{model_name}.csv"


def get_coeffsbydecs_path(model_name: str) -> Path:
    return FIGURES_DIR / f"expl_coeffbydecs_{model_name}.svg"


def get_resids_path(model_name: str) -> Path:
    return FIGURES_DIR / f"expl_resids_{model_name}.svg"


def get_statssum_path(model_name: str, industry: str) -> Path:
    # Use .strip() to avoid trailing spaces in industry names (e.g., 'Hlth ')
    clean_ind = industry.strip()
    return OTHER_DIR / f"expl_statssum_{model_name}_{clean_ind}.txt"


def get_comp_path(model_type: str) -> Path:
    return FIGURES_DIR / f"pred_comp_{model_type}.svg"
