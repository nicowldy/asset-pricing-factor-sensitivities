"""RMSE and out-of-sample R² per model and industry."""

import numpy as np
import pandas as pd

from asset_pricing.config import MODELS, OOS_METRICS_TABLE, PREDICTIONS
from asset_pricing.data.storage import read_marked_csv
from asset_pricing.modeling.out_of_sample.plots import plot_r2_bar, plot_rmse_bar
from asset_pricing.modeling.tables import write_table


def main():
    df = pd.concat([read_marked_csv(PREDICTIONS[m]) for m in MODELS], ignore_index=True)
    metrics = []
    for industry in df["industry"].unique():
        for model in MODELS:
            subset = df[(df.model == model) & (df.industry == industry)]
            y_true = subset["actual_excess"]
            sq_err = (y_true - subset["expected_excess"]) ** 2
            ss_res = sq_err.sum()
            ss_tot = ((y_true - y_true.mean()) ** 2).sum()
            metrics.append(
                {
                    "model": model,
                    "industry": industry,
                    "r2": 1 - ss_res / ss_tot if ss_tot > 0 else np.nan,
                    "rmse": np.sqrt(sq_err.mean()),
                }
            )

    df_metrics = pd.DataFrame(metrics)
    # Rows are ordered CAPM, FF3, FF5 within each industry: delta to the smaller model.
    deltas = df_metrics.groupby("industry", sort=False)[["r2", "rmse"]].diff()
    df_metrics[["r2_delta", "rmse_delta"]] = deltas.to_numpy()
    write_table(df_metrics, OOS_METRICS_TABLE)

    plot_r2_bar(df_metrics.rename(columns={"model": "Model", "r2": "R2"}))
    plot_rmse_bar(df_metrics.rename(columns={"model": "Model", "rmse": "RMSE"}))


if __name__ == "__main__":
    main()
