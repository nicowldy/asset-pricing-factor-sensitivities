import os
from pathlib import Path

try:
    from src.config import (
        PROJECT_ROOT,
        REPORTS_DIR,
        FIGURES_DIR,
        TABLES_DIR,
        OTHER_DIR,
        DESCRIPT_IND_TABLE as DESCRIPT_IND,
        FIG_RSQ as RSQ,
        FIG_DISTRIB_IND as DISTRIB_IND,
        FIG_DISTRIB_FACT as DISTRIB_FACT,
        ASSUMPTIONS_TABLE as ASSUMPTIONS,
        INCRWALD_CAPM_TABLE as INCRWALD_CAPM,
        INCRWALD_FF3_TABLE as INCRWALD_FF3,
        FIG_RSQBYDECS as RSQBYDECS,
        FIG_ALPHABYDECS as ALPHABYDECS,
        FIG_CUMRETURNS_FACT as CUMRETURNS_FACT,
        FIG_CUMRETURNS_IND as CUMRETURNS_IND,
        JOINTWALD_CAPM_TABLE as JOINTWALD,
        FF_CAPM_PROCESSED,
        FF_FF3_PROCESSED,
        FF_FF5_PROCESSED,
        FF_IND_PROCESSED,
        get_descript_model_path as _get_descript_model_path,
        get_params_path as _get_params_path,
        get_coeffsbydecs_path as _get_coeffsbydecs_path,
        get_resids_path as _get_resids_path,
        get_statssum_path as _get_statssum_path,
    )
    BASE_DIR = PROJECT_ROOT
    RETURNS = FIGURES_DIR / "expl_returns.svg"

    def get_descript_model_path(model_name):
        return str(_get_descript_model_path(model_name))

    def get_params_path(model_name):
        return str(_get_params_path(model_name))

    def get_coeffsbydecs_path(model_name):
        return str(_get_coeffsbydecs_path(model_name))

    def get_resids_path(model_name):
        return str(_get_resids_path(model_name))

    def get_statssum_path(model_name, industry):
        return str(_get_statssum_path(model_name, industry))

    PROJECT_ROOT = str(PROJECT_ROOT)
    BASE_DIR = str(BASE_DIR)
    REPORTS_DIR = str(REPORTS_DIR)
    FIGURES_DIR = str(FIGURES_DIR)
    TABLES_DIR = str(TABLES_DIR)
    OTHER_DIR = str(OTHER_DIR)
    DESCRIPT_IND = str(DESCRIPT_IND)
    RSQ = str(RSQ)
    RETURNS = str(RETURNS)
    DISTRIB_IND = str(DISTRIB_IND)
    DISTRIB_FACT = str(DISTRIB_FACT)
    ASSUMPTIONS = str(ASSUMPTIONS)
    INCRWALD_CAPM = str(INCRWALD_CAPM)
    INCRWALD_FF3 = str(INCRWALD_FF3)
    RSQBYDECS = str(RSQBYDECS)
    ALPHABYDECS = str(ALPHABYDECS)
    CUMRETURNS_FACT = str(CUMRETURNS_FACT)
    CUMRETURNS_IND = str(CUMRETURNS_IND)
    JOINTWALD = str(JOINTWALD)
    FF_CAPM_PROCESSED = str(FF_CAPM_PROCESSED)
    FF_FF3_PROCESSED = str(FF_FF3_PROCESSED)
    FF_FF5_PROCESSED = str(FF_FF5_PROCESSED)
    FF_IND_PROCESSED = str(FF_IND_PROCESSED)

except ModuleNotFoundError:
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))
    BASE_DIR = PROJECT_ROOT
    REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
    FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")
    TABLES_DIR = os.path.join(REPORTS_DIR, "tables")
    OTHER_DIR = os.path.join(REPORTS_DIR, "other")

    DESCRIPT_IND = os.path.join(TABLES_DIR, "expl_descript_ind.csv")
    RSQ = os.path.join(FIGURES_DIR, "expl_rsq.svg")
    RETURNS = os.path.join(FIGURES_DIR, "expl_returns.svg")
    DISTRIB_IND = os.path.join(FIGURES_DIR, "expl_distrib_ind.svg")
    DISTRIB_FACT = os.path.join(FIGURES_DIR, "expl_distrib_fact.svg")
    ASSUMPTIONS = os.path.join(TABLES_DIR, "expl_assumptions.csv")
    INCRWALD_CAPM = os.path.join(TABLES_DIR, "expl_incrwald_capm.csv")
    INCRWALD_FF3 = os.path.join(TABLES_DIR, "expl_incrwald_ff3.csv")
    RSQBYDECS = os.path.join(FIGURES_DIR, "expl_rsqbydecs.svg")
    ALPHABYDECS = os.path.join(FIGURES_DIR, "expl_alphabydecs.svg")
    CUMRETURNS_FACT = os.path.join(FIGURES_DIR, "expl_cumreturns_fact.svg")
    CUMRETURNS_IND = os.path.join(FIGURES_DIR, "expl_cumreturns_ind.svg")
    JOINTWALD = os.path.join(TABLES_DIR, "expl_jointwald.csv")

    def get_descript_model_path(model_name):
        return os.path.join(TABLES_DIR, f"expl_descript_{model_name}.csv")

    def get_params_path(model_name):
        return os.path.join(TABLES_DIR, f"expl_regress_{model_name}.csv")

    def get_coeffsbydecs_path(model_name):
        return os.path.join(FIGURES_DIR, f"expl_coeffbydecs_{model_name}.svg")

    def get_resids_path(model_name):
        return os.path.join(FIGURES_DIR, f"expl_resids_{model_name}.svg")

    def get_statssum_path(model_name, industry):
        return os.path.join(OTHER_DIR, f"expl_statssum_{model_name}_{industry.strip()}.txt")

    FF_CAPM_PROCESSED = os.path.join(BASE_DIR, "data", "processed", "ff_capm_processed.csv")
    FF_FF3_PROCESSED = os.path.join(BASE_DIR, "data", "processed", "ff_ff3_processed.csv")
    FF_FF5_PROCESSED = os.path.join(BASE_DIR, "data", "processed", "ff_ff5_processed.csv")
    FF_IND_PROCESSED = os.path.join(BASE_DIR, "data", "processed", "ff_ind_processed.csv")
