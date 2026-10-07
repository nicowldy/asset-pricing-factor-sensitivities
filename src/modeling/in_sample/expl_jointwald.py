import os
import pandas as pd
import numpy as np
from scipy import stats  # type: ignore[import-untyped]

from src.modeling.in_sample.expl_utils import (
    get_industry_names,
    load_industry_data,
    add_average_row,
    run_regression,
    load_factors,
    calculate_excess_returns,
    get_models,
)
from src.modeling.in_sample.expl_config import TABLES_DIR
from src.modeling.in_sample.expl_tables import write_jointwald_results


def perform_joint_wald_test(factor_data, industry_data, factor_names, industry):
    results = run_regression(
        factor_data, industry_data, factor_names, industry, cov_type="HAC"
    )

    param_names = results.params.index.tolist()
    factor_indices = [param_names.index(factor) for factor in factor_names]
    q = len(factor_indices)

    beta = results.params
    cov_matrix = results.cov_params()

    k_total = len(param_names)
    R = np.zeros((q, k_total))
    for i, idx in enumerate(factor_indices):
        R[i, idx] = 1

    Rbeta = R @ beta
    RcovR = R @ cov_matrix @ R.T
    wald_stat = Rbeta.T @ np.linalg.inv(RcovR) @ Rbeta

    p_value = 1 - stats.chi2.cdf(wald_stat, q)

    return float(wald_stat), float(p_value)


def main():
    os.makedirs(TABLES_DIR, exist_ok=True)

    industry_data = load_industry_data()
    industry_names = get_industry_names(industry_data)

    models = get_models()
    factor_data_capm = load_factors("capm")
    factor_data_ff3 = load_factors("ff3")
    factor_data_ff5 = load_factors("ff5")
    industry_data_excess = calculate_excess_returns(industry_data, factor_data_capm)

    results_capm = []
    results_ff3 = []
    results_ff5 = []

    for industry in industry_names:
        wald_capm, p_capm = perform_joint_wald_test(
            factor_data_capm, industry_data_excess, models["capm"]["factors"], industry
        )
        capm_reg = run_regression(
            factor_data_capm,
            industry_data_excess,
            models["capm"]["factors"],
            industry,
            cov_type="HAC",
        )
        results_capm.append(
            {
                "industry": industry,
                "adj_r2": capm_reg.rsquared_adj,
                "wald_stat": wald_capm,
                "p_value": p_capm,
            }
        )

        wald_ff3, p_ff3 = perform_joint_wald_test(
            factor_data_ff3, industry_data_excess, models["ff3"]["factors"], industry
        )
        ff3_reg = run_regression(
            factor_data_ff3,
            industry_data_excess,
            models["ff3"]["factors"],
            industry,
            cov_type="HAC",
        )
        results_ff3.append(
            {
                "industry": industry,
                "adj_r2": ff3_reg.rsquared_adj,
                "wald_stat": wald_ff3,
                "p_value": p_ff3,
            }
        )

        wald_ff5, p_ff5 = perform_joint_wald_test(
            factor_data_ff5, industry_data_excess, models["ff5"]["factors"], industry
        )
        ff5_reg = run_regression(
            factor_data_ff5,
            industry_data_excess,
            models["ff5"]["factors"],
            industry,
            cov_type="HAC",
        )
        results_ff5.append(
            {
                "industry": industry,
                "adj_r2": ff5_reg.rsquared_adj,
                "wald_stat": wald_ff5,
                "p_value": p_ff5,
            }
        )

    df_capm = add_average_row(pd.DataFrame(results_capm))
    df_ff3 = add_average_row(pd.DataFrame(results_ff3))
    df_ff5 = add_average_row(pd.DataFrame(results_ff5))

    write_jointwald_results(df_capm, df_ff3, df_ff5)


if __name__ == "__main__":
    main()
