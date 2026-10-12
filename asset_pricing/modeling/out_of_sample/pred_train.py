import pandas as pd
import statsmodels.api as sm

from asset_pricing.config import FF_IND_PROCESSED, MODELS, PROCESSED, TRAINED
from asset_pricing.data.data_utils import load_data_with_markers, save_with_markers
from asset_pricing.modeling.in_sample.expl_utils import get_industry_names


def train_models_and_export(model_type):
    factors = MODELS[model_type]["factors"]
    df_f = load_data_with_markers(PROCESSED[model_type])
    df_i = load_data_with_markers(FF_IND_PROCESSED)
    n_folds = max(len(df_f) - 24, 0)
    coefs = []

    for fold in range(1, n_folds + 1):
        train_f = df_f.iloc[: 23 + fold]
        train_i = df_i.iloc[: 23 + fold]
        for ind in get_industry_names(train_i):
            y = train_i[ind] - train_f["RF"]
            X = sm.add_constant(train_f[factors])
            res = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 12})
            params = res.params.to_dict()
            params.update(industry=ind, fold=fold, model=model_type)
            coefs.append(params)
    save_with_markers(pd.DataFrame(coefs), TRAINED[model_type])


def main():
    for m in MODELS:
        train_models_and_export(m)


if __name__ == "__main__":
    main()
