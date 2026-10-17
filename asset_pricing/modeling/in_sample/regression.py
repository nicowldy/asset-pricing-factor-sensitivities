"""Full-sample OLS regressions of the industry excess returns on the factors."""

import re

import pandas as pd
from statsmodels.api import OLS, add_constant
from statsmodels.stats.stattools import durbin_watson, jarque_bera

from asset_pricing.config import FIG_ADJ_R2, MODELS, REGRESSION_TABLE, summary_path
from asset_pricing.data.loaders import (
    calculate_excess_returns,
    get_industry_names,
    load_factors,
    load_industry_data,
)
from asset_pricing.modeling.in_sample.plots import plot_adj_r2
from asset_pricing.modeling.tables import add_average_row, write_table


def run_regression(factor_data, industry_data, factor_names, industry, cov_type="HAC"):
    excess_col = f"{industry}_Excess"
    if excess_col not in industry_data.columns:
        available = [
            col.replace("_Excess", "")
            for col in industry_data.columns
            if col.endswith("_Excess")
        ]
        raise KeyError(f"Industry '{industry}' not found. Available: {available}")
    y = industry_data[excess_col]
    X = add_constant(factor_data[factor_names])
    if cov_type == "HAC":
        return OLS(y, X).fit(cov_type=cov_type, cov_kwds={"maxlags": 12})
    return OLS(y, X).fit(cov_type=cov_type)  # type: ignore


def get_regression_parameters(results):
    params = results.params
    bse = results.bse
    pvals = results.pvalues
    return {
        "results": results,
        "residuals": results.resid,
        "fitted": results.fittedvalues,
        "r_squared": results.rsquared,
        "adj_r_squared": results.rsquared_adj,
        "f_statistic": results.fvalue,
        "f_pvalue": results.f_pvalue,
        "alpha": params.get("const"),
        "alpha_std_err": bse.get("const"),
        "alpha_p_value": pvals.get("const"),
        "betas": {k: v for k, v in params.items() if k != "const"},
        "betas_se": {k: bse[k] for k in bse.index if k != "const"},
        "betas_pvalue": {k: pvals[k] for k in pvals.index if k != "const"},
    }


def run_all_regressions(industry_data=None):
    """Regression parameters per model and industry, by default on the full sample."""
    if industry_data is None:
        industry_data = load_industry_data()
    all_results = {}
    for model_name, info in MODELS.items():
        factor_data = load_factors(model_name).loc[industry_data.index]
        data_excess = calculate_excess_returns(industry_data, factor_data)
        all_results[model_name] = {
            industry: get_regression_parameters(
                run_regression(factor_data, data_excess, info["factors"], industry)
            )
            for industry in get_industry_names(industry_data)
        }
    return all_results


def collect_industry_statistics(reg_params, industry, factors):
    jb_stat, jb_pvalue, _, _ = jarque_bera(reg_params["residuals"])
    stats = {
        "Industry": industry,
        "Alpha": reg_params["alpha"],
        "Alpha_p_value": reg_params["alpha_p_value"],
        "Alpha_std_err": reg_params["alpha_std_err"],
        "R_squared": reg_params["r_squared"],
        "Adj_R_squared": reg_params["adj_r_squared"],
        "F_statistic": reg_params["f_statistic"],
        "F_pvalue": reg_params["f_pvalue"],
        "Durbin_Watson": durbin_watson(reg_params["residuals"]),
        "JB_statistic": jb_stat,
        "JB_pvalue": jb_pvalue,
    }
    for f in factors:
        stats[f"{f}_coef"] = reg_params["betas"][f]
        stats[f"{f}_p_value"] = reg_params["betas_pvalue"][f]
        stats[f"{f}_std_err"] = reg_params["betas_se"][f]
    return stats


def model_statistics(model_name, model_results):
    """One row of regression statistics per industry."""
    factors = MODELS[model_name]["factors"]
    return pd.DataFrame(
        [
            collect_industry_statistics(params, industry, factors)
            for industry, params in model_results.items()
        ]
    )


def save_regression_summary(model_name, industry, results):
    path = summary_path(model_name, industry)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Blank the run timestamp so the summary is reproducible byte-for-byte.
    summary = re.sub(
        r"^(Date|Time):(\s+)(\S.*?)(?=\s{3})",
        lambda m: f"{m[1]}:{m[2]}{' ' * len(m[3])}",
        results.summary().as_text(),
        flags=re.MULTILINE,
    )
    with open(path, "w") as f:
        f.write(f"Regression Summary for {model_name} on {industry}\n\n")
        f.write(summary)


def main():
    all_results = run_all_regressions()
    for model_name, model_results in all_results.items():
        for industry, params in model_results.items():
            save_regression_summary(model_name, industry, params["results"])
        write_table(
            add_average_row(model_statistics(model_name, model_results)),
            REGRESSION_TABLE[model_name],
        )
    plot_adj_r2(all_results, save_path=FIG_ADJ_R2)


if __name__ == "__main__":
    main()
