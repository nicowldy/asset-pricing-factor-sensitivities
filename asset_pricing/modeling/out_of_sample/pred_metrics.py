import numpy as np
import pandas as pd

from asset_pricing.config import PRED_METRICS_TABLE, TESTED
from asset_pricing.data.data_utils import load_data_with_markers
from asset_pricing.modeling.out_of_sample.pred_plots import plot_r2_bar, plot_rmse_bar


def main():
    df = pd.concat(
        [load_data_with_markers(path) for path in TESTED.values()],
        ignore_index=True,
    )

    models_order = ["capm", "ff3", "ff5"]
    metrics = []

    for industry in df["industry"].unique():
        for model in models_order:
            subset = df[(df.model == model) & (df.industry == industry)]
            if subset.empty:
                continue

            y_true = subset["actual_excess"]
            y_pred = subset["expected_excess"]

            rmse = np.sqrt(((y_true - y_pred) ** 2).mean())
            ss_res = ((y_true - y_pred) ** 2).sum()
            ss_tot = ((y_true - y_true.mean()) ** 2).sum()
            r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan

            metrics.append(
                {
                    "model": model,
                    "industry": industry,
                    "r2": r2,
                    "rmse": rmse,
                }
            )

    for entry in metrics:
        idx = models_order.index(entry["model"])
        if idx == 0:
            entry["r2_delta"] = np.nan
            entry["rmse_delta"] = np.nan
        else:
            prev_model = models_order[idx - 1]
            ref = next(
                e
                for e in metrics
                if e["industry"] == entry["industry"] and e["model"] == prev_model
            )
            entry["r2_delta"] = entry["r2"] - ref["r2"]
            entry["rmse_delta"] = entry["rmse"] - ref["rmse"]

    df_metrics = pd.DataFrame(metrics)
    PRED_METRICS_TABLE.parent.mkdir(parents=True, exist_ok=True)
    df_metrics.to_csv(PRED_METRICS_TABLE, index=False)

    plot_r2_bar(
        df_metrics.rename(
            columns={"model": "Model", "industry": "industry", "r2": "R2"}
        )
    )
    plot_rmse_bar(
        df_metrics.rename(
            columns={"model": "Model", "industry": "industry", "rmse": "RMSE"}
        )
    )


if __name__ == "__main__":
    main()
