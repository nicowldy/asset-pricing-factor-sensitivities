"""Paths and model definitions for the whole pipeline."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
INTERIM_DIR = DATA_DIR / "interim"

REPORTS_DIR = PROJECT_ROOT / "reports"
TABLES_DIR = REPORTS_DIR / "tables"
FIGURES_DIR = REPORTS_DIR / "figures"
SUMMARIES_DIR = REPORTS_DIR / "summaries"

MODELS = {
    "capm": {"factors": ["MKT"]},
    "ff3": {"factors": ["MKT", "SMB", "HML"]},
    "ff5": {"factors": ["MKT", "SMB", "HML", "RMW", "CMA"]},
}

# Raw input from the Kenneth R. French Data Library
DATA_DATE = "2025-02-24"
FF3_RAW = RAW_DIR / f"ff_ff3_monthly_pct_raw_{DATA_DATE}.csv"
FF5_RAW = RAW_DIR / f"ff_ff5_monthly_pct_raw_{DATA_DATE}.csv"
INDUSTRY_RAW = RAW_DIR / f"ff_ind_monthly_pct_raw_{DATA_DATE}.csv"

# Stage 1: data
FACTORS_PROCESSED = {m: PROCESSED_DIR / f"{m}_factors.csv" for m in MODELS}
INDUSTRY_PROCESSED = PROCESSED_DIR / "industry_returns.csv"
SAMPLE_TABLE = TABLES_DIR / "data_sample.csv"

DATASETS = [
    # CAPM has no raw file of its own: MKT and RF come from the FF3 file.
    {
        "name": "capm",
        "input": FF3_RAW,
        "output": FACTORS_PROCESSED["capm"],
        "columns": ["MKT", "RF"],
    },
    {"name": "ff3", "input": FF3_RAW, "output": FACTORS_PROCESSED["ff3"]},
    {"name": "ff5", "input": FF5_RAW, "output": FACTORS_PROCESSED["ff5"]},
    {"name": "ind", "input": INDUSTRY_RAW, "output": INDUSTRY_PROCESSED},
]

# Stage 2: in-sample
DESCRIPTIVE_FACTORS_TABLE = {m: TABLES_DIR / f"descriptive_{m}.csv" for m in MODELS}
DESCRIPTIVE_INDUSTRIES_TABLE = TABLES_DIR / "descriptive_industries.csv"
FIG_DISTRIBUTION_FACTORS = FIGURES_DIR / "descriptive_distribution_factors.svg"
FIG_DISTRIBUTION_INDUSTRIES = FIGURES_DIR / "descriptive_distribution_industries.svg"
FIG_CUMULATIVE_FACTORS = FIGURES_DIR / "descriptive_cumulative_returns_factors.svg"
FIG_CUMULATIVE_INDUSTRIES = (
    FIGURES_DIR / "descriptive_cumulative_returns_industries.svg"
)

REGRESSION_TABLE = {m: TABLES_DIR / f"in_sample_regression_{m}.csv" for m in MODELS}
WALD_JOINT_TABLE = {m: TABLES_DIR / f"in_sample_wald_joint_{m}.csv" for m in MODELS}
WALD_CAPM_FF3_TABLE = TABLES_DIR / "in_sample_wald_incremental_capm_ff3.csv"
WALD_FF3_FF5_TABLE = TABLES_DIR / "in_sample_wald_incremental_ff3_ff5.csv"
DIAGNOSTICS_TABLE = TABLES_DIR / "in_sample_diagnostics.csv"

FIG_ADJ_R2 = FIGURES_DIR / "in_sample_adj_r2.svg"
FIG_RESIDUALS = {m: FIGURES_DIR / f"in_sample_residuals_{m}.svg" for m in MODELS}
FIG_ADJ_R2_BY_DECADE = FIGURES_DIR / "in_sample_adj_r2_by_decade.svg"
FIG_ALPHA_BY_DECADE = FIGURES_DIR / "in_sample_alpha_by_decade.svg"
FIG_BETAS_BY_DECADE = {
    m: FIGURES_DIR / f"in_sample_betas_by_decade_{m}.svg" for m in MODELS
}


def summary_path(model_name: str, industry: str) -> Path:
    # The raw industry file names one column "Hlth " with a trailing space.
    return SUMMARIES_DIR / f"in_sample_summary_{model_name}_{industry.strip()}.txt"


# Stage 3: out-of-sample
COEFFICIENTS = {m: INTERIM_DIR / f"{m}_coefficients.csv" for m in MODELS}
PREDICTIONS = {m: INTERIM_DIR / f"{m}_predictions.csv" for m in MODELS}

OOS_METRICS_TABLE = TABLES_DIR / "out_of_sample_metrics.csv"
OOS_ERROR_TTEST_TABLE = TABLES_DIR / "out_of_sample_error_ttest.csv"
OOS_PAIRED_TTEST_TABLE = TABLES_DIR / "out_of_sample_paired_ttest.csv"

FIG_OOS_R2 = FIGURES_DIR / "out_of_sample_r2.svg"
FIG_OOS_RMSE = FIGURES_DIR / "out_of_sample_rmse.svg"
FIG_OOS_ACTUAL_VS_PREDICTED = {
    m: FIGURES_DIR / f"out_of_sample_actual_vs_predicted_{m}.svg" for m in MODELS
}
FIG_OOS_ACTUAL_VS_PREDICTED_EXAMPLES = (
    FIGURES_DIR / "out_of_sample_actual_vs_predicted_examples.svg"
)
