from __future__ import annotations

from asset_pricing.config import FIG_RSQ
from asset_pricing.modeling.in_sample.expl_plots import plot_rsq
from asset_pricing.modeling.in_sample.expl_utils import run_regression_analysis


def run_analysis(save_outputs: bool = True):
    all_results, all_model_stats = run_regression_analysis(save_outputs=save_outputs)
    if save_outputs:
        plot_rsq(all_results, save_path=FIG_RSQ)
    return all_results, all_model_stats


if __name__ == "__main__":
    run_analysis(save_outputs=True)
