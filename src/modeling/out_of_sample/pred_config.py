"""Out-of-sample predictive configuration re-exporting from central src.config."""
from __future__ import annotations

from src.config import (
    DATA_DIR,
    FF_CAPM_PROCESSED as PROCESSED_CAPM_DIR,
    FF_FF3_PROCESSED as PROCESSED_FF3_DIR,
    FF_FF5_PROCESSED as PROCESSED_FF5_DIR,
    FF_IND_PROCESSED as PROCESSED_IND_DIR,
    FIG_PRED_COMPEXAM as COMPEXAM,
    FIG_PRED_RMSE as RMSE,
    FIG_PRED_RSQ as RSQ,
    MODELS,
    PRED_METRICS_TABLE as METRICS,
    PRED_PAIRTTEST_TABLE as PAIRTTEST,
    PRED_TTEST_TABLE as TTEST,
    PROJECT_ROOT,
    TABLES_DIR,
    TESTED,
    TRAINED,
    get_comp_path,
)
