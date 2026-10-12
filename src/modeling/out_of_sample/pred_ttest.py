"""Out-of-sample prediction error t-tests with Newey-West HAC covariance."""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm

from src.config import MODELS, PRED_TTEST_TABLE, TESTED
from src.data.data_utils import load_data_with_markers


def _perform_ttest_on_group(group: pd.DataFrame) -> dict[str, float]:
    errors = group["error"].dropna()
    if len(errors) < 2:
        return {"t_statistic": np.nan, "p_value": np.nan}

    y = errors
    X = np.ones(len(y))

    model = sm.OLS(y, X)
    results = model.fit(cov_type="HAC", cov_kwds={"maxlags": 12})

    t_stat = float(np.asarray(results.tvalues)[0])
    p_val = float(np.asarray(results.pvalues)[0])

    return {"t_statistic": t_stat, "p_value": p_val}


def calculate_t_test_for_model(model_type: str) -> pd.DataFrame:
    df_tested = load_data_with_markers(TESTED[model_type])
    if df_tested.empty:
        return pd.DataFrame()

    results = []
    for ind, group in df_tested.groupby("industry"):
        res = _perform_ttest_on_group(group)
        if not np.isnan(res["t_statistic"]):
            results.append(
                {
                    "model": model_type,
                    "industry": ind,
                    "t_statistic": res["t_statistic"],
                    "p_value": res["p_value"],
                }
            )

    return pd.DataFrame(results)[["model", "industry", "t_statistic", "p_value"]]


def main() -> None:
    all_ttest_results = []
    for model_key in MODELS:
        model_results_df = calculate_t_test_for_model(model_key)
        if not model_results_df.empty:
            all_ttest_results.append(model_results_df)

    if not all_ttest_results:
        return

    df_final_results = pd.concat(all_ttest_results, ignore_index=True)

    PRED_TTEST_TABLE.parent.mkdir(parents=True, exist_ok=True)
    df_final_results.to_csv(PRED_TTEST_TABLE, index=False)


if __name__ == "__main__":
    main()
