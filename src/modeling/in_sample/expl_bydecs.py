from src.modeling.in_sample.expl_utils import (
    load_industry_data,
    get_models,
    filter_data_by_period,
    run_regression_by_decade,
    process_model_statistics,
    get_decades,
)
from src.modeling.in_sample.expl_config import RSQBYDECS, ALPHABYDECS
from src.modeling.in_sample.expl_plots import (
    plot_decade_rsquared_grid,
    plot_decade_model_factor_grids,
    plot_decade_model_alpha_grids,
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
                    save_outputs=True,
                )
                df["Decade"] = decade_name
                decade_stats[model_name] = df

        all_decade_results[decade_name] = decade_results
        all_decade_stats[decade_name] = decade_stats

    plot_decade_rsquared_grid(all_decade_stats, decades_order, True, RSQBYDECS)
    for model_name in models:
        plot_decade_model_factor_grids(all_decade_results, decades_order, True)
    plot_decade_model_alpha_grids(all_decade_results, decades_order, True, ALPHABYDECS)


if __name__ == "__main__":
    main()
