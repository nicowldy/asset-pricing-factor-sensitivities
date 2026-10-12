from __future__ import annotations

from src.config import (
    ASSUMPTIONS_TABLE,
    DESCRIPT_IND_TABLE,
    INCRWALD_CAPM_TABLE,
    INCRWALD_FF3_TABLE,
    get_descript_model_path,
    get_jointwald_path,
    get_params_path,
)
from src.modeling.in_sample.expl_utils import add_average_row


def _write(df, path, index=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=index)


def write_model_statistics(model_name, model_df):
    _write(add_average_row(model_df), get_params_path(model_name))


def write_incrwald_results(df_ff3_ff5, df_capm_ff3):
    _write(df_ff3_ff5, INCRWALD_FF3_TABLE)
    _write(df_capm_ff3, INCRWALD_CAPM_TABLE)


def write_jointwald_results(model_name, df):
    """Save the joint Wald test results for intra-model significance testing."""
    _write(df, get_jointwald_path(model_name))


def write_descriptive_stats_model(model_name, stats):
    _write(stats, get_descript_model_path(model_name), index=True)


def write_descriptive_stats_industry(stats):
    _write(stats, DESCRIPT_IND_TABLE, index=True)


def write_assumption_results(df):
    _write(df, ASSUMPTIONS_TABLE)
