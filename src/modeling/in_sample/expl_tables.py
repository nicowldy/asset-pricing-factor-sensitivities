from __future__ import annotations

import os
from src.config import TABLES_DIR
from src.modeling.in_sample.expl_config import (
    ASSUMPTIONS,
    DESCRIPT_IND,
    INCRWALD_CAPM,
    INCRWALD_FF3,
    get_descript_model_path,
    get_params_path,
)
from src.modeling.in_sample.expl_utils import add_average_row


def write_model_statistics(model_name, model_df):
    df = add_average_row(model_df)
    path = get_params_path(model_name)
    os.makedirs(os.path.dirname(str(path)), exist_ok=True)
    df.to_csv(path, index=False)


def write_incrwald_results(df_ff3_ff5, df_capm_ff3):
    os.makedirs(os.path.dirname(str(INCRWALD_FF3)), exist_ok=True)
    df_ff3_ff5.to_csv(INCRWALD_FF3, index=False)
    df_capm_ff3.to_csv(INCRWALD_CAPM, index=False)


def write_jointwald_results(df_capm, df_ff3, df_ff5):
    """Save the joint Wald test results for intra-model significance testing."""
    capm_path = os.path.join(str(TABLES_DIR), "expl_jointwald_capm.csv")
    ff3_path = os.path.join(str(TABLES_DIR), "expl_jointwald_ff3.csv")
    ff5_path = os.path.join(str(TABLES_DIR), "expl_jointwald_ff5.csv")

    os.makedirs(str(TABLES_DIR), exist_ok=True)

    df_capm.to_csv(capm_path, index=False)
    df_ff3.to_csv(ff3_path, index=False)
    df_ff5.to_csv(ff5_path, index=False)


def write_descriptive_stats_model(model_name, stats):
    path = get_descript_model_path(model_name)
    os.makedirs(os.path.dirname(str(path)), exist_ok=True)
    stats.to_csv(path)


def write_descriptive_stats_industry(stats):
    os.makedirs(os.path.dirname(str(DESCRIPT_IND)), exist_ok=True)
    stats.to_csv(DESCRIPT_IND)


def write_assumption_results(df):
    path = ASSUMPTIONS
    os.makedirs(os.path.dirname(str(path)), exist_ok=True)
    df.to_csv(path, index=False)
