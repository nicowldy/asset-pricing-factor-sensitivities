"""The full-sample regressions repeated for each decade; produces figures only."""

from asset_pricing.config import FIG_ADJ_R2_BY_DECADE, FIG_ALPHA_BY_DECADE
from asset_pricing.data.loaders import load_industry_data
from asset_pricing.modeling.in_sample.plots import (
    plot_decade_model_alpha_grids,
    plot_decade_model_factor_grids,
    plot_decade_rsquared_grid,
)
from asset_pricing.modeling.in_sample.regression import (
    model_statistics,
    run_all_regressions,
)

DECADES = {
    "1970s": ("1970-01-01", "1979-12-31"),
    "1980s": ("1980-01-01", "1989-12-31"),
    "1990s": ("1990-01-01", "1999-12-31"),
    "2000s": ("2000-01-01", "2009-12-31"),
    "2010s": ("2010-01-01", "2019-12-31"),
}


def main():
    industry_data = load_industry_data()
    all_decade_results = {}
    all_decade_stats = {}

    for decade, (start, end) in DECADES.items():
        results = run_all_regressions(industry_data.loc[start:end])
        all_decade_results[decade] = results
        all_decade_stats[decade] = {
            model_name: model_statistics(model_name, model_results)
            for model_name, model_results in results.items()
        }

    decades_order = list(DECADES)
    plot_decade_rsquared_grid(all_decade_stats, decades_order, FIG_ADJ_R2_BY_DECADE)
    plot_decade_model_factor_grids(all_decade_results, decades_order)
    plot_decade_model_alpha_grids(
        all_decade_results, decades_order, FIG_ALPHA_BY_DECADE
    )


if __name__ == "__main__":
    main()
