"""Out-of-sample prediction error t-tests with Newey-West HAC covariance."""
from __future__ import annotations

import os
import numpy as np
import pandas as pd
import statsmodels.api as sm

try:
    from src.modeling.out_of_sample.pred_config import MODELS, TESTED, TTEST
    from src.modeling.out_of_sample.pred_utils import load_data_with_markers
except (ModuleNotFoundError, ImportError):
    try:
        from .pred_config import MODELS, TESTED, TTEST
        from .pred_utils import load_data_with_markers
    except (ImportError, ValueError):
        from pred_config import MODELS, TESTED, TTEST  # type: ignore[import-not-found]
        from pred_utils import load_data_with_markers  # type: ignore[import-not-found]


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
            results.append({
                "model": model_type,
                "industry": ind,
                "t_statistic": res["t_statistic"],
                "p_value": res["p_value"],
            })

    return pd.DataFrame(results)[["model", "industry", "t_statistic", "p_value"]]


def main() -> None:
    all_ttest_results = []
    for model_key in MODELS.keys():
        model_results_df = calculate_t_test_for_model(model_key)
        if not model_results_df.empty:
            all_ttest_results.append(model_results_df)

    if not all_ttest_results:
        return

    df_final_results = pd.concat(all_ttest_results, ignore_index=True)

    output_dir = os.path.dirname(TTEST)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    df_final_results.to_csv(TTEST, index=False)


if __name__ == "__main__":
    main()
