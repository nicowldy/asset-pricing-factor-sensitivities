"""Estimate the factor loadings on an expanding window, one fold per month."""

import pandas as pd
import statsmodels.api as sm

from asset_pricing.config import (
    COEFFICIENTS,
    FACTORS_PROCESSED,
    INDUSTRY_PROCESSED,
    MODELS,
)
from asset_pricing.data.loaders import get_industry_names
from asset_pricing.data.storage import read_marked_csv, write_marked_csv

FIRST_WINDOW = 24


def estimate_coefficients(model_name):
    """Fold k is estimated on the first FIRST_WINDOW + k - 1 months."""
    factors = MODELS[model_name]["factors"]
    df_f = read_marked_csv(FACTORS_PROCESSED[model_name])
    df_i = read_marked_csv(INDUSTRY_PROCESSED)
    coefs = []

    for fold in range(1, len(df_f) - FIRST_WINDOW + 1):
        train_f = df_f.iloc[: FIRST_WINDOW - 1 + fold]
        train_i = df_i.iloc[: FIRST_WINDOW - 1 + fold]
        for ind in get_industry_names(train_i):
            y = train_i[ind] - train_f["RF"]
            X = sm.add_constant(train_f[factors])
            res = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 12})
            params = res.params.to_dict()
            params.update(industry=ind, fold=fold, model=model_name)
            coefs.append(params)
    write_marked_csv(pd.DataFrame(coefs), COEFFICIENTS[model_name])


def main():
    for m in MODELS:
        estimate_coefficients(m)


if __name__ == "__main__":
    main()
