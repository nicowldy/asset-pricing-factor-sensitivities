import pandas as pd
import statsmodels.api as sm
import os
try:
    from src.modeling.out_of_sample.pred_config import (
        MODELS,
        PROCESSED_CAPM_DIR,
        PROCESSED_FF3_DIR,
        PROCESSED_FF5_DIR,
        PROCESSED_IND_DIR,
        TRAINED,
    )
    from src.modeling.out_of_sample.pred_utils import get_industry_names, load_data_with_markers
except ModuleNotFoundError:
    try:
        from modeling.out_of_sample.pred_config import (
            MODELS,
            PROCESSED_CAPM_DIR,
            PROCESSED_FF3_DIR,
            PROCESSED_FF5_DIR,
            PROCESSED_IND_DIR,
            TRAINED,
        )
        from modeling.out_of_sample.pred_utils import get_industry_names, load_data_with_markers
    except ModuleNotFoundError:
        from pred_config import (
            MODELS,
            PROCESSED_CAPM_DIR,
            PROCESSED_FF3_DIR,
            PROCESSED_FF5_DIR,
            PROCESSED_IND_DIR,
            TRAINED,
        )
        from pred_utils import get_industry_names, load_data_with_markers


processed_dirs = {
    "capm": PROCESSED_CAPM_DIR,
    "ff3": PROCESSED_FF3_DIR,
    "ff5": PROCESSED_FF5_DIR,
}


def train_models_and_export(model_type):
    factors = MODELS[model_type]["factors"]
    data_type = MODELS[model_type]["data_type"]
    df_f = load_data_with_markers(processed_dirs[data_type])
    df_i = load_data_with_markers(PROCESSED_IND_DIR)
    n_folds = max(len(df_f) - 24, 0)
    if n_folds == 0:
        return pd.DataFrame()
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
    df_coefs = pd.DataFrame(coefs)
    out_path = TRAINED[model_type]
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write("#data-begin#\n")
        f.write(df_coefs.to_csv(index=False))
        f.write("#data-end#\n")


def main():
    for m in MODELS:
        train_models_and_export(m)


if __name__ == "__main__":
    main()
