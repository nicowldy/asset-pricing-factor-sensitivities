from asset_pricing.config import FIG_ALPHABYDECS, FIG_RSQBYDECS
from asset_pricing.modeling.in_sample.expl_plots import (
    plot_decade_model_alpha_grids,
    plot_decade_model_factor_grids,
    plot_decade_rsquared_grid,
)
from asset_pricing.modeling.in_sample.expl_utils import (
    filter_data_by_period,
    get_decades,
    get_models,
    load_industry_data,
    process_model_statistics,
    run_regression_by_decade,
)


def main():
    industry_data = load_industry_data()
    models = get_models()
    decades = get_decades()
    decades_order = list(decades.keys())
    all_decade_results = {}
    all_decade_stats = {}

    for decade_name, period in decades.items():
        decade_results = {}
        decade_stats = {}

        for model_name, model_info in models.items():
            res = run_regression_by_decade(
                model_name,
                model_info,
                industry_data,
                period,
            )
            decade_results[model_name] = res

            if res:
                df = process_model_statistics(
                    model_name,
                    model_info,
                    decade_results,
                    filter_data_by_period(industry_data, *period),
                    # Full-sample tables and summaries belong to expl_regress.
                    save_outputs=False,
                )
                df["Decade"] = decade_name
                decade_stats[model_name] = df

        all_decade_results[decade_name] = decade_results
        all_decade_stats[decade_name] = decade_stats

    plot_decade_rsquared_grid(all_decade_stats, decades_order, True, FIG_RSQBYDECS)
    plot_decade_model_factor_grids(all_decade_results, decades_order, True)
    plot_decade_model_alpha_grids(
        all_decade_results, decades_order, True, FIG_ALPHABYDECS
    )


if __name__ == "__main__":
    main()
