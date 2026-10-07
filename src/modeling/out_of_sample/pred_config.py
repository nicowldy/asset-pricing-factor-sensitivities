import os
from pathlib import Path

try:
    from src.config import (
        PROJECT_ROOT,
        DATA_DIR,
        FF_IND_PROCESSED as PROCESSED_IND_DIR,
        FF_CAPM_PROCESSED as PROCESSED_CAPM_DIR,
        FF_FF3_PROCESSED as PROCESSED_FF3_DIR,
        FF_FF5_PROCESSED as PROCESSED_FF5_DIR,
        MODELS as _MODELS,
        FIG_PRED_RSQ as RSQ,
        FIG_PRED_RMSE as RMSE,
        TABLES_DIR,
        TRAINED as _TRAINED,
        TESTED as _TESTED,
        PRED_METRICS_TABLE as METRICS,
        PRED_TTEST_TABLE as TTEST,
        PRED_PAIRTTEST_TABLE as PAIRTTEST,
        FIG_PRED_COMPEXAM as COMPEXAM,
        get_comp_path as _get_comp_path,
    )

    MODELS = {k: {"factors": v["factors"], "data_type": v["data_type"]} for k, v in _MODELS.items()}
    TRAINED = {k: str(v) for k, v in _TRAINED.items()}
    TESTED = {k: str(v) for k, v in _TESTED.items()}
    PROJECT_ROOT = str(PROJECT_ROOT)
    DATA_DIR = str(DATA_DIR)
    PROCESSED_IND_DIR = str(PROCESSED_IND_DIR)
    PROCESSED_CAPM_DIR = str(PROCESSED_CAPM_DIR)
    PROCESSED_FF3_DIR = str(PROCESSED_FF3_DIR)
    PROCESSED_FF5_DIR = str(PROCESSED_FF5_DIR)
    RSQ = str(RSQ)
    RMSE = str(RMSE)
    TABLES_DIR = str(TABLES_DIR)
    METRICS = str(METRICS)
    TTEST = str(TTEST)
    PAIRTTEST = str(PAIRTTEST)
    COMPEXAM = str(COMPEXAM)

    def get_comp_path(model_type):
        return str(_get_comp_path(model_type))

except ModuleNotFoundError:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
    DATA_DIR = os.path.join(PROJECT_ROOT, "data")

    PROCESSED_IND_DIR = os.path.join(DATA_DIR, "processed", "ff_ind_processed.csv")
    PROCESSED_CAPM_DIR = os.path.join(DATA_DIR, "processed", "ff_capm_processed.csv")
    PROCESSED_FF3_DIR = os.path.join(DATA_DIR, "processed", "ff_ff3_processed.csv")
    PROCESSED_FF5_DIR = os.path.join(DATA_DIR, "processed", "ff_ff5_processed.csv")

    MODELS = {
        "capm": {"factors": ["MKT"], "data_type": "capm"},
        "ff3": {"factors": ["MKT", "SMB", "HML"], "data_type": "ff3"},
        "ff5": {"factors": ["MKT", "SMB", "HML", "RMW", "CMA"], "data_type": "ff5"},
    }

    RSQ = os.path.join(PROJECT_ROOT, "reports", "figures", "pred_rsq.svg")
    RMSE = os.path.join(PROJECT_ROOT, "reports", "figures", "pred_rmse.svg")
    TABLES_DIR = os.path.join(PROJECT_ROOT, "reports", "tables")

    TRAINED = {
        m: os.path.join(PROJECT_ROOT, "data", "interim", f"ff_{m}_trained.csv")
        for m in MODELS
    }
    TESTED = {
        m: os.path.join(PROJECT_ROOT, "data", "interim", f"ff_{m}_tested.csv")
        for m in MODELS
    }

    METRICS = os.path.join(PROJECT_ROOT, "reports", "tables", "pred_metrics.csv")
    TTEST = os.path.join(PROJECT_ROOT, "reports", "tables", "pred_ttest.csv")
    PAIRTTEST = os.path.join(PROJECT_ROOT, "reports", "tables", "pred_pairttest.csv")
    COMPEXAM = os.path.join(PROJECT_ROOT, "reports", "figures", "pred_compexample.svg")

    def get_comp_path(model_type):
        return os.path.join(
            PROJECT_ROOT, "reports", "figures", f"pred_comp_{model_type}.svg"
        )
