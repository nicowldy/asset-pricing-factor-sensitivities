import os

import numpy as np
import pandas as pd
import statsmodels.api as sm

try:
    from src.modeling.out_of_sample.pred_config import MODELS, TESTED, TTEST
    from src.modeling.out_of_sample.pred_utils import load_data_with_markers
except ModuleNotFoundError:
    try:
        from modeling.out_of_sample.pred_config import MODELS, TESTED, TTEST
        from modeling.out_of_sample.pred_utils import load_data_with_markers
    except ModuleNotFoundError:
        from pred_config import MODELS, TESTED, TTEST
        from pred_utils import load_data_with_markers



def _perform_ttest_on_group(group):
    errors = group["error"].dropna()
    if len(errors) < 2:
        return pd.Series({"t_statistic": pd.NA, "p_value": pd.NA})

    y = errors
    X = np.ones(len(y))

    model = sm.OLS(y, X)
    results = model.fit(cov_type="HAC", cov_kwds={"maxlags": 12})
    t_statistic = results.tvalues.iloc[0]
    p_value = results.pvalues.iloc[0]

    return pd.Series({"t_statistic": t_statistic, "p_value": p_value})


def calculate_t_test_for_model(model_type):
    df_tested = load_data_with_markers(TESTED[model_type])

    results_df = (
        df_tested.groupby("industry")
        .apply(_perform_ttest_on_group, include_groups=False)
        .dropna(subset=["t_statistic"])
    )

    results_df = results_df.reset_index()
    results_df["model"] = model_type
    return results_df[["model", "industry", "t_statistic", "p_value"]]


def main():
    all_ttest_results = []
    for model_key in MODELS.keys():
        model_results_df = calculate_t_test_for_model(model_key)
        if not model_results_df.empty:
            all_ttest_results.append(model_results_df)

    df_final_results = pd.concat(all_ttest_results, ignore_index=True)

    output_dir = os.path.dirname(TTEST)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    df_final_results.to_csv(TTEST, index=False)


if __name__ == "__main__":
    main()
