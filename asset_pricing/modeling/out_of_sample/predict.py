"""Apply the coefficients of each fold to the factor returns of the following month."""

import pandas as pd

from asset_pricing.config import (
    COEFFICIENTS,
    FACTORS_PROCESSED,
    INDUSTRY_PROCESSED,
    MODELS,
    PREDICTIONS,
)
from asset_pricing.data.loaders import get_industry_names
from asset_pricing.data.storage import read_marked_csv, write_marked_csv
from asset_pricing.modeling.out_of_sample.estimate import FIRST_WINDOW


def predict(model_name):
    df_coefs = read_marked_csv(COEFFICIENTS[model_name])
    df_ind = read_marked_csv(INDUSTRY_PROCESSED)
    df_f = read_marked_csv(FACTORS_PROCESSED[model_name])
    factors = MODELS[model_name]["factors"]
    results = []

    for fold in range(1, len(df_f) - FIRST_WINDOW + 1):
        # The first month after the estimation window of this fold
        idx = FIRST_WINDOW - 1 + fold
        x_f = df_f.iloc[idx]
        rf = x_f["RF"]
        for ind in get_industry_names(df_ind):
            ind_return = df_ind[ind].iloc[idx]
            actual = ind_return - rf
            row = df_coefs.query(
                "fold == @fold and model == @model_name and industry == @ind"
            )
            if row.empty:
                continue
            p = row.iloc[0]
            exp = p.get("const", 0) + sum(p.get(f, 0) * x_f[f] for f in factors)
            results.append(
                dict(
                    fold=fold,
                    model=model_name,
                    industry=ind,
                    industry_return=ind_return,
                    risk_free_rate=rf,
                    actual_excess=actual,
                    expected_excess=exp,
                    error=actual - exp,
                )
            )
    write_marked_csv(pd.DataFrame(results), PREDICTIONS[model_name])


def main():
    for m in MODELS:
        predict(m)


if __name__ == "__main__":
    main()
