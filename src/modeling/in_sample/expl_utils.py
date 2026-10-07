import io
import os

import pandas as pd
from scipy.stats import pearsonr  # type: ignore[import-untyped]
from scipy import stats  # type: ignore[import-untyped]
from statsmodels.api import OLS, add_constant
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson, jarque_bera
from statsmodels.tsa.stattools import adfuller

try:
    from src.modeling.in_sample.expl_config import (
        FF_CAPM_PROCESSED,
        FF_FF3_PROCESSED,
        FF_FF5_PROCESSED,
        FF_IND_PROCESSED,
        get_statssum_path,
    )
except (ModuleNotFoundError, ImportError):
    try:
        from .expl_config import (
            FF_CAPM_PROCESSED,
            FF_FF3_PROCESSED,
            FF_FF5_PROCESSED,
            FF_IND_PROCESSED,
            get_statssum_path,
        )
    except (ImportError, ValueError):
        from expl_config import (  # type: ignore[import-not-found]
            FF_CAPM_PROCESSED,
            FF_FF3_PROCESSED,
            FF_FF5_PROCESSED,
            FF_IND_PROCESSED,
            get_statssum_path,
        )


MODELS = {
    "capm": {"factors": ["MKT"], "file_path": FF_CAPM_PROCESSED},
    "ff3": {"factors": ["MKT", "SMB", "HML"], "file_path": FF_FF3_PROCESSED},
    "ff5": {
        "factors": ["MKT", "SMB", "HML", "RMW", "CMA"],
        "file_path": FF_FF5_PROCESSED,
    },
}


def load_data(file_path):
    with open(file_path, "r") as file:
        data = file.read()
    start = data.find("#data-begin#") + len("#data-begin#")
    end = data.find("#data-end#")
    df = pd.read_csv(io.StringIO(data[start:end].strip()))
    df["Date"] = pd.to_datetime(df["Date"], format="%Y%m")
    return df.set_index("Date")


def load_industry_data():
    return load_data(FF_IND_PROCESSED)


def get_models():
    return MODELS


def load_factors(model_name):
    return load_data(MODELS[model_name]["file_path"])


def get_industry_names(industry_data):
    return [col for col in industry_data.columns if not col.endswith("_Excess")]


def calculate_excess_returns(industry_data, factor_data):
    result = industry_data.copy()
    for industry in get_industry_names(industry_data):
        result[f"{industry}_Excess"] = industry_data[industry] - factor_data["RF"]
    return result


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
    alpha = params.get("const")
    alpha_se = bse.get("const")
    alpha_pvalue = pvals.get("const")
    betas = {k: v for k, v in params.items() if k != "const"}
    betas_se = {k: bse[k] for k in bse.index if k != "const"}
    betas_pvalue = {k: pvals[k] for k in pvals.index if k != "const"}
    return {
        "residuals": results.resid,
        "fitted": results.fittedvalues,
        "r_squared": results.rsquared,
        "adj_r_squared": results.rsquared_adj,
        "f_statistic": results.fvalue,
        "f_pvalue": results.f_pvalue,
        "alpha": alpha,
        "alpha_std_err": alpha_se,
        "alpha_p_value": alpha_pvalue,
        "betas": betas,
        "betas_se": betas_se,
        "betas_pvalue": betas_pvalue,
    }


def run_all_regressions(cov_type="HAC"):
    industry_data = load_industry_data()
    industries = get_industry_names(industry_data)
    models = get_models()
    all_results = {}
    for model_name, info in models.items():
        factor_data = load_factors(model_name)
        data_excess = calculate_excess_returns(industry_data, factor_data)
        all_results[model_name] = {
            industry: get_regression_parameters(
                run_regression(
                    factor_data, data_excess, info["factors"], industry, cov_type
                )
            )
            for industry in industries
        }
    return all_results


def collect_industry_statistics(reg_params, industry, factors):
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
    }
    jb = jarque_bera(reg_params["residuals"])
    stats["JB_statistic"] = jb[0]
    stats["JB_pvalue"] = jb[1]
    for f in factors:
        stats[f"{f}_coef"] = reg_params["betas"][f]
        stats[f"{f}_p_value"] = reg_params["betas_pvalue"][f]
        stats[f"{f}_std_err"] = reg_params["betas_se"][f]
    return stats


def add_average_row(model_df):
    numeric = model_df.select_dtypes(include=["number"]).columns
    avg = {"Industry": "Average"}
    for col in numeric:
        avg[col] = model_df[col].mean()
    return pd.concat([model_df, pd.DataFrame([avg])], ignore_index=True)


def save_regression_summary(model_name, industry, results):
    path = get_statssum_path(model_name, industry)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(f"Regression Summary for {model_name} on {industry}\n\n")
        f.write(results.summary().as_text())


def process_model_statistics(
    model_name, model_info, all_results, industry_data, save_outputs=True
):
    factors = model_info["factors"]
    industries = get_industry_names(industry_data)
    stats_list = []
    for industry in industries:
        reg = all_results[model_name][industry]
        if save_outputs:
            fd_full = load_factors(model_name)
            start, end = industry_data.index.min(), industry_data.index.max()
            fd = filter_data_by_period(fd_full, start, end)
            ide = calculate_excess_returns(industry_data, fd)
            res = run_regression(fd, ide, factors, industry)
            save_regression_summary(model_name, industry, res)
        stats_list.append(collect_industry_statistics(reg, industry, factors))
    df = pd.DataFrame(stats_list)
    if save_outputs:
        try:
            from src.modeling.in_sample.expl_tables import write_model_statistics
        except (ModuleNotFoundError, ImportError):
            try:
                from .expl_tables import write_model_statistics
            except (ImportError, ValueError):
                from expl_tables import write_model_statistics  # type: ignore[import-not-found]

        write_model_statistics(model_name, df)
    return df


def run_regression_analysis(save_outputs=True):
    all_results = run_all_regressions()
    models = get_models()
    industry_data = load_industry_data()
    all_model_stats = {}
    for name, info in models.items():
        all_model_stats[name] = process_model_statistics(
            name, info, all_results, industry_data, save_outputs
        )
    return all_results, all_model_stats


def calculate_rss(residuals):
    return (residuals**2).sum()


def filter_data_by_period(df, start, end):
    return df.loc[start:end]


def get_decades():
    return {
        "1970s": ("1970-01-01", "1979-12-31"),
        "1980s": ("1980-01-01", "1989-12-31"),
        "1990s": ("1990-01-01", "1999-12-31"),
        "2000s": ("2000-01-01", "2009-12-31"),
        "2010s": ("2010-01-01", "2019-12-31"),
    }


def run_regression_by_decade(
    model_name, model_info, industry_data, period, cov_type="HAC"
):
    start, end = period
    ind = filter_data_by_period(industry_data, start, end)
    fac = filter_data_by_period(load_factors(model_name), start, end)
    excess = calculate_excess_returns(ind, fac)
    return {
        industry: get_regression_parameters(
            run_regression(fac, excess, model_info["factors"], industry, cov_type)
        )
        for industry in get_industry_names(ind)
    }


def calculate_descriptive_stats(df):
    """Calculate descriptive statistics for each column, including skewness and kurtosis."""
    desc = df.describe().transpose()
    desc["skew"] = df.skew()
    desc["kurtosis"] = df.kurtosis()
    return desc.transpose()


def test_multicollinearity(X):
    vif_data = pd.DataFrame(
        {
            "Variable": X.columns,
            "VIF": [variance_inflation_factor(X.values, i) for i in range(X.shape[1])],
        }
    )
    max_vif = vif_data["VIF"].max()
    return {"vif_data": vif_data, "max_vif": max_vif, "passed": max_vif < 10}


def test_linearity(results):
    corr, pvalue = pearsonr(results.fittedvalues, results.resid)
    return {"correlation": corr, "passed": pvalue > 0.05}  # type: ignore


def test_independence(results):
    dw = durbin_watson(results.resid)
    return {"dw_stat": dw, "dw_passed": abs(dw - 2) < 0.5}


def test_homoskedasticity(results):
    lm_stat, lm_pvalue, _, _ = het_breuschpagan(results.resid, results.model.exog)
    return {"bp_stat": lm_stat, "bp_pvalue": lm_pvalue, "passed": lm_pvalue > 0.05}


def test_stationarity(series):
    adf_stat, pvalue, _, _, _, _ = adfuller(series.dropna())  # type: ignore
    return {"adf_stat": adf_stat, "adf_pvalue": pvalue, "passed": pvalue < 0.05}


def perform_hac_wald_test(
    factor_data, industry_data, industry, restricted_factors, unrestricted_factors
):
    import numpy as np

    unrestricted_results = run_regression(
        factor_data, industry_data, unrestricted_factors, industry, cov_type="HAC"
    )

    additional_factors = [
        f for f in unrestricted_factors if f not in restricted_factors
    ]
    q = len(additional_factors)

    param_names = unrestricted_results.params.index.tolist()
    restriction_indices = [param_names.index(factor) for factor in additional_factors]

    beta = unrestricted_results.params
    cov_matrix = unrestricted_results.cov_params()

    k_total = len(param_names)
    R = np.zeros((q, k_total))
    for i, idx in enumerate(restriction_indices):
        R[i, idx] = 1

    Rbeta = R @ beta
    RcovR = R @ cov_matrix @ R.T
    wald_stat = Rbeta.T @ np.linalg.inv(RcovR) @ Rbeta

    p_value = 1 - stats.chi2.cdf(wald_stat, q)

    return float(wald_stat), float(p_value)
