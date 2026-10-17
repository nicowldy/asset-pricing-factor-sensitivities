"""Checks of the OLS assumptions per model and industry, plus residual plots."""

import pandas as pd
from scipy.stats import pearsonr  # type: ignore[import-untyped]
from statsmodels.api import add_constant
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson
from statsmodels.tsa.stattools import adfuller

from asset_pricing.config import DIAGNOSTICS_TABLE, FIG_RESIDUALS, MODELS
from asset_pricing.data.loaders import load_factors, load_industry_data
from asset_pricing.modeling.in_sample.plots import plot_residuals_fitted_grid
from asset_pricing.modeling.in_sample.regression import run_all_regressions
from asset_pricing.modeling.tables import write_table


def check_multicollinearity(X):
    vif = pd.Series(
        [variance_inflation_factor(X.values, i) for i in range(X.shape[1])],
        index=X.columns,
    )
    return {"vif": vif, "max_vif": vif.max(), "passed": vif.max() < 10}


def check_linearity(results):
    corr, pvalue = pearsonr(results.fittedvalues, results.resid)
    return {"correlation": corr, "passed": pvalue > 0.05}  # type: ignore


def check_independence(results):
    dw = durbin_watson(results.resid)
    return {"dw_stat": dw, "passed": abs(dw - 2) < 0.5}


def check_homoskedasticity(results):
    lm_stat, lm_pvalue, _, _ = het_breuschpagan(results.resid, results.model.exog)
    return {"bp_stat": lm_stat, "bp_pvalue": lm_pvalue, "passed": lm_pvalue > 0.05}


def check_stationarity(series):
    adf_stat, pvalue, _, _, _, _ = adfuller(series.dropna(), result_object=False)  # type: ignore
    return {"adf_stat": adf_stat, "adf_pvalue": pvalue, "passed": pvalue < 0.05}


def main():
    all_results = run_all_regressions()
    industry_data = load_industry_data()
    rows = []

    for model_name, model_info in MODELS.items():
        factor_data = load_factors(model_name)
        multi = check_multicollinearity(
            add_constant(factor_data[model_info["factors"]])
        )

        for industry, params in all_results[model_name].items():
            results = params["results"]
            lin = check_linearity(results)
            ind = check_independence(results)
            homo = check_homoskedasticity(results)
            stat = check_stationarity(industry_data[industry] - factor_data["RF"])
            checks = [lin, ind, homo, multi, stat]
            tests_passed = sum(c["passed"] for c in checks)

            row = {
                "model": model_name,
                "industry": industry,
                "cov_type": "HAC",
                "linearity_correlation": lin["correlation"],
                "linearity_passed": lin["passed"],
                "dw_stat": ind["dw_stat"],
                "autocorrelation_passed": ind["passed"],
                "bp_stat": homo["bp_stat"],
                "bp_pvalue": homo["bp_pvalue"],
                "homoskedasticity_passed": homo["passed"],
                "max_vif": multi["max_vif"],
                "multicollinearity_passed": multi["passed"],
                "adf_stat": stat["adf_stat"],
                "adf_pvalue": stat["adf_pvalue"],
                "stationarity_passed": stat["passed"],
                "tests_passed": tests_passed,
                "tests_failed": len(checks) - tests_passed,
                "all_tests_passed": tests_passed == len(checks),
            }
            for factor, vif in multi["vif"].drop("const").items():
                row[f"vif_{factor}"] = vif
            rows.append(row)

        plot_residuals_fitted_grid(
            all_results[model_name], save_path=FIG_RESIDUALS[model_name]
        )

    write_table(pd.DataFrame(rows), DIAGNOSTICS_TABLE)


if __name__ == "__main__":
    main()
