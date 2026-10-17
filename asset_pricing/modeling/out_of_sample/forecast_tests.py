"""t-tests on the out-of-sample prediction errors with Newey-West HAC covariance."""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm

from asset_pricing.config import (
    MODELS,
    OOS_ERROR_TTEST_TABLE,
    OOS_PAIRED_TTEST_TABLE,
    PREDICTIONS,
)
from asset_pricing.data.storage import read_marked_csv
from asset_pricing.modeling.tables import write_table

MODEL_PAIRS = [("capm", "ff3"), ("ff3", "ff5")]


def hac_mean_ttest(series: pd.Series) -> tuple[float, float]:
    """t-statistic and two-sided p-value of H0: mean of `series` is zero (HAC)."""
    y = series.dropna()
    results = sm.OLS(y, np.ones(len(y))).fit(cov_type="HAC", cov_kwds={"maxlags": 12})
    return float(np.asarray(results.tvalues)[0]), float(np.asarray(results.pvalues)[0])


def error_ttest(predictions: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Two-sided test per model and industry that the mean error is zero."""
    rows = []
    for model_name, df in predictions.items():
        for ind, group in df.groupby("industry"):
            t_stat, p_value = hac_mean_ttest(group["error"])
            rows.append(
                {
                    "model": model_name,
                    "industry": ind,
                    "t_statistic": t_stat,
                    "p_value": p_value,
                }
            )
    return pd.DataFrame(rows)


def paired_ttest(predictions: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """One-sided test that model B has smaller squared errors than model A."""
    errors = {
        m: df.set_index(["industry", "fold"])["error"] for m, df in predictions.items()
    }
    industries = sorted(errors["capm"].index.get_level_values("industry").unique())

    rows = []
    for ind in industries:
        for model_a, model_b in MODEL_PAIRS:
            diff_sq = errors[model_a].loc[ind].pow(2) - errors[model_b].loc[ind].pow(2)
            t_stat, p_two_sided = hac_mean_ttest(diff_sq)
            rows.append(
                {
                    "industry": ind,
                    "model_A": model_a,
                    "model_B": model_b,
                    "t_statistic": t_stat,
                    "p_value": p_two_sided / 2 if t_stat >= 0 else 1 - p_two_sided / 2,
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    predictions = {m: read_marked_csv(PREDICTIONS[m]) for m in MODELS}
    write_table(error_ttest(predictions), OOS_ERROR_TTEST_TABLE)
    write_table(paired_ttest(predictions), OOS_PAIRED_TTEST_TABLE)


if __name__ == "__main__":
    main()
