import os
import pandas as pd

from src.modeling.out_of_sample.pred_config import (
    MODELS,
    PROCESSED_CAPM_DIR,
    PROCESSED_FF3_DIR,
    PROCESSED_FF5_DIR,
    PROCESSED_IND_DIR,
    TRAINED,
    TESTED,
)
from src.modeling.out_of_sample.pred_utils import (
    load_data_with_markers,
    get_industry_names,
)


processed_dirs = {
    "capm": PROCESSED_CAPM_DIR,
    "ff3": PROCESSED_FF3_DIR,
    "ff5": PROCESSED_FF5_DIR,
}


def test_models_and_export(model_type):
    df_coefs = load_data_with_markers(TRAINED[model_type])
    df_ind = load_data_with_markers(PROCESSED_IND_DIR)
    df_fs = {dt: load_data_with_markers(fp) for dt, fp in processed_dirs.items()}
    factors = MODELS[model_type]["factors"]
    df_f = df_fs[MODELS[model_type]["data_type"]]
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
    df_out = pd.DataFrame(results)
    out_path = TESTED[model_type]
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write("#data-begin#\n")
        f.write(df_out.to_csv(index=False))
        f.write("#data-end#\n")


def main():
    for m in MODELS:
        test_models_and_export(m)


if __name__ == "__main__":
    main()
