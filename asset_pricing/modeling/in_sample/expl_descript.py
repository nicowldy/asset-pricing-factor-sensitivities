from asset_pricing.config import (
    FIG_CUMRETURNS_FACT,
    FIG_CUMRETURNS_IND,
    FIG_DISTRIB_FACT,
    FIG_DISTRIB_IND,
)
from asset_pricing.modeling.in_sample.expl_plots import (
    plot_cumulative_log_factor_returns,
    plot_cumulative_log_industry_returns,
    plot_factor_distributions,
    plot_industry_distributions,
)
from asset_pricing.modeling.in_sample.expl_tables import (
    write_descriptive_stats_industry,
    write_descriptive_stats_model,
)
from asset_pricing.modeling.in_sample.expl_utils import (
    calculate_descriptive_stats,
    get_industry_names,
    get_models,
    load_factors,
    load_industry_data,
)


def calculate_and_save_descriptive_stats():
    models = get_models()
    for model_name in models:
        factor_data = load_factors(model_name)
        stats = calculate_descriptive_stats(factor_data)
        write_descriptive_stats_model(model_name, stats)

    industry_data = load_industry_data()
    industry_names = get_industry_names(industry_data)
    industry_df = industry_data[industry_names]
    stats = calculate_descriptive_stats(industry_df)
    write_descriptive_stats_industry(stats)

    return industry_data, industry_names


def run_all_analyses(save_plots=True):
    calculate_and_save_descriptive_stats()
    plot_industry_distributions(save_path=FIG_DISTRIB_IND if save_plots else None)
    plot_factor_distributions(save_path=FIG_DISTRIB_FACT if save_plots else None)
    plot_cumulative_log_factor_returns(
        save_path=FIG_CUMRETURNS_FACT if save_plots else None
    )
    plot_cumulative_log_industry_returns(
        save_path=FIG_CUMRETURNS_IND if save_plots else None
    )


if __name__ == "__main__":
    run_all_analyses(save_plots=True)
