"""Scatter plots of actual against predicted excess returns."""

from asset_pricing.config import MODELS, PREDICTIONS
from asset_pricing.data.storage import read_marked_csv
from asset_pricing.modeling.out_of_sample.plots import (
    plot_actual_vs_pred,
    plot_actual_vs_pred_examples,
)


def _actual_vs_expected(model):
    """Actual and expected excess returns of one model, keyed by industry."""
    df = read_marked_csv(PREDICTIONS[model])
    return {
        ind: grp.rename(
            columns={"actual_excess": "Actual", "expected_excess": "Expected"}
        )[["Actual", "Expected"]]
        for ind, grp in df.groupby("industry")
    }


def main():
    for m in MODELS:
        plot_actual_vs_pred(_actual_vs_expected(m), m)
    plot_actual_vs_pred_examples(
        _actual_vs_expected("ff5"), industries=("Manuf", "Utils")
    )


if __name__ == "__main__":
    main()
