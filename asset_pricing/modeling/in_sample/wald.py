"""Joint and incremental Wald tests on the HAC-estimated factor loadings."""

import numpy as np
import pandas as pd
from scipy import stats  # type: ignore[import-untyped]

from asset_pricing.config import (
    MODELS,
    WALD_CAPM_FF3_TABLE,
    WALD_FF3_FF5_TABLE,
    WALD_JOINT_TABLE,
)
from asset_pricing.modeling.in_sample.regression import run_all_regressions
from asset_pricing.modeling.tables import add_average_row, write_table


def wald_test(results, factor_names):
    """Wald test that the coefficients on `factor_names` are jointly zero.

    Uses the covariance matrix of `results`, so the test is HAC-robust when the
    regression was fitted with HAC standard errors.
    """
    beta = results.params[factor_names].to_numpy()
    cov = results.cov_params().loc[factor_names, factor_names].to_numpy()
    wald_stat = beta.T @ np.linalg.inv(cov) @ beta
    p_value = 1 - stats.chi2.cdf(wald_stat, len(factor_names))
    return float(wald_stat), float(p_value)


def joint_wald(all_results, model_name):
    """Per industry: are all factor loadings of the model zero?"""
    rows = []
    for industry, params in all_results[model_name].items():
        wald_stat, p_value = wald_test(params["results"], MODELS[model_name]["factors"])
        rows.append(
            {
                "industry": industry,
                "adj_r2": params["adj_r_squared"],
                "wald_stat": wald_stat,
                "p_value": p_value,
            }
        )
    return add_average_row(pd.DataFrame(rows))


def incremental_wald(all_results, smaller, larger):
    """Per industry: are the factors that `larger` adds to `smaller` zero?"""
    added = [
        f for f in MODELS[larger]["factors"] if f not in MODELS[smaller]["factors"]
    ]
    rows = []
    for industry, params in all_results[larger].items():
        wald_stat, p_value = wald_test(params["results"], added)
        r2_smaller = all_results[smaller][industry]["adj_r_squared"]
        rows.append(
            {
                "industry": industry,
                f"adj_r2_{smaller}": r2_smaller,
                f"adj_r2_{larger}": params["adj_r_squared"],
                "delta_adj_r2": params["adj_r_squared"] - r2_smaller,
                "wald_stat": wald_stat,
                "p_value": p_value,
            }
        )
    return add_average_row(pd.DataFrame(rows))


def main():
    all_results = run_all_regressions()
    for model_name in MODELS:
        write_table(joint_wald(all_results, model_name), WALD_JOINT_TABLE[model_name])
    write_table(incremental_wald(all_results, "capm", "ff3"), WALD_CAPM_FF3_TABLE)
    write_table(incremental_wald(all_results, "ff3", "ff5"), WALD_FF3_FF5_TABLE)


if __name__ == "__main__":
    main()
