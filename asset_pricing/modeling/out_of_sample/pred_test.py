import pandas as pd

from asset_pricing.config import FF_IND_PROCESSED, MODELS, PROCESSED, TESTED, TRAINED
from asset_pricing.data.data_utils import load_data_with_markers, save_with_markers
from asset_pricing.modeling.in_sample.expl_utils import get_industry_names


def test_models_and_export(model_type):
    df_coefs = load_data_with_markers(TRAINED[model_type])
    df_ind = load_data_with_markers(FF_IND_PROCESSED)
    df_f = load_data_with_markers(PROCESSED[model_type])
    factors = MODELS[model_type]["factors"]
    n_folds = max(len(df_f) - 24, 0)
    results = []

    for fold in range(1, n_folds + 1):
        idx = 23 + fold
        x_f = df_f.iloc[idx]
        rf = x_f["RF"]
        for ind in get_industry_names(df_ind):
            ind_return = df_ind[ind].iloc[idx]
            actual = ind_return - rf
            row = df_coefs.query(
                "fold == @fold and model == @model_type and industry == @ind"
            )
            if row.empty:
                continue
            p = row.iloc[0]
            exp = p.get("const", 0) + sum(p.get(f, 0) * x_f[f] for f in factors)
            results.append(
                dict(
                    fold=fold,
                    model=model_type,
                    industry=ind,
                    industry_return=ind_return,
                    risk_free_rate=rf,
                    actual_excess=actual,
                    expected_excess=exp,
                    error=actual - exp,
                )
            )
    save_with_markers(pd.DataFrame(results), TESTED[model_type])


def main():
    for m in MODELS:
        test_models_and_export(m)


if __name__ == "__main__":
    main()
