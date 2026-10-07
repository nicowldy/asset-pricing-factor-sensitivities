import pandas as pd
import statsmodels.api as sm
import numpy as np
import os
try:
    from src.modeling.out_of_sample.pred_config import MODELS, TESTED, PAIRTTEST
    from src.modeling.out_of_sample.pred_utils import load_data_with_markers
except ModuleNotFoundError:
    try:
        from modeling.out_of_sample.pred_config import MODELS, TESTED, PAIRTTEST
        from modeling.out_of_sample.pred_utils import load_data_with_markers
    except ModuleNotFoundError:
        from pred_config import MODELS, TESTED, PAIRTTEST
        from pred_utils import load_data_with_markers



def calculate_paired_t_test():
    model_errors = {}
    for model_key in MODELS.keys():
        df_tested = load_data_with_markers(TESTED[model_key])
        if not df_tested.empty:
            model_errors[model_key] = df_tested.set_index(["industry", "fold"])["error"]

    if len(model_errors) < 2:
        return pd.DataFrame()

    paired_results = []
    specific_model_pairs = [("capm", "ff3"), ("ff3", "ff5")]

    all_industries = set()
    for errors_df in model_errors.values():
        all_industries.update(errors_df.index.get_level_values("industry").unique())

    for ind in all_industries:
        for model_a_key, model_b_key in specific_model_pairs:
            if model_a_key not in model_errors or model_b_key not in model_errors:
                continue

            errors_a = model_errors[model_a_key].get(ind, pd.Series(dtype="float64"))
            errors_b = model_errors[model_b_key].get(ind, pd.Series(dtype="float64"))

            if errors_a.empty or errors_b.empty:
                continue

            common_folds = errors_a.index.intersection(errors_b.index)
            if len(common_folds) < 2:
                continue

            errors_a_aligned = errors_a.loc[common_folds]
            errors_b_aligned = errors_b.loc[common_folds]

            diff_sq = errors_a_aligned.pow(2) - errors_b_aligned.pow(2)
            diff_sq.dropna(inplace=True)

            if len(diff_sq) >= 2:
                y = diff_sq
                X = np.ones(len(y))
                model = sm.OLS(y, X)
                results = model.fit(cov_type="HAC", cov_kwds={"maxlags": 12})
                t_stat_sq = float(np.asarray(results.tvalues)[0])
                p_val_two_sided = float(np.asarray(results.pvalues)[0])

                if t_stat_sq >= 0:
                    p_val_sq = p_val_two_sided / 2
                else:
                    p_val_sq = 1 - p_val_two_sided / 2

                paired_results.append(
                    {
                        "industry": ind,
                        "model_A": model_a_key,
                        "model_B": model_b_key,
                        "t_statistic": t_stat_sq,
                        "p_value": p_val_sq,
                    }
                )

    return pd.DataFrame(paired_results)


def main():
    df_paired_results = calculate_paired_t_test()

    output_dir_paired = os.path.dirname(PAIRTTEST)
    os.makedirs(output_dir_paired, exist_ok=True)
    df_paired_results.to_csv(PAIRTTEST, index=False)


if __name__ == "__main__":
    main()
