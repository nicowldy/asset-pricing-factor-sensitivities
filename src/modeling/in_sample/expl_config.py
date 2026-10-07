"""In-sample econometric configuration re-exporting from central src.config."""
from __future__ import annotations

from src.config import (
    ASSUMPTIONS_TABLE as ASSUMPTIONS,
    DESCRIPT_IND_TABLE as DESCRIPT_IND,
    FF_CAPM_PROCESSED,
    FF_FF3_PROCESSED,
    FF_FF5_PROCESSED,
    FF_IND_PROCESSED,
    FIGURES_DIR,
    FIG_ALPHABYDECS as ALPHABYDECS,
    FIG_CUMRETURNS_FACT as CUMRETURNS_FACT,
    FIG_CUMRETURNS_IND as CUMRETURNS_IND,
    FIG_DISTRIB_FACT as DISTRIB_FACT,
    FIG_DISTRIB_IND as DISTRIB_IND,
    FIG_RSQ as RSQ,
    FIG_RSQBYDECS as RSQBYDECS,
    INCRWALD_CAPM_TABLE as INCRWALD_CAPM,
    INCRWALD_FF3_TABLE as INCRWALD_FF3,
    JOINTWALD_CAPM_TABLE as JOINTWALD,
    OTHER_DIR,
    PROJECT_ROOT,
    REPORTS_DIR,
    TABLES_DIR,
    get_coeffsbydecs_path,
    get_descript_model_path,
    get_params_path,
    get_resids_path,
    get_statssum_path,
)

BASE_DIR = PROJECT_ROOT
