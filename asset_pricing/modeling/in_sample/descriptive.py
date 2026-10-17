"""Descriptive statistics, return distributions and cumulative returns."""

from asset_pricing.config import (
    CORRELATIONS_TABLE,
    DESCRIPTIVE_FACTORS_TABLE,
    DESCRIPTIVE_INDUSTRIES_TABLE,
    FIG_CUMULATIVE_FACTORS,
    FIG_CUMULATIVE_INDUSTRIES,
    FIG_DISTRIBUTION_FACTORS,
    FIG_DISTRIBUTION_INDUSTRIES,
    MODELS,
)
from asset_pricing.data.loaders import (
    get_industry_names,
    load_factors,
    load_industry_data,
)
from asset_pricing.modeling.in_sample.plots import (
    plot_cumulative_log_factor_returns,
    plot_cumulative_log_industry_returns,
    plot_factor_distributions,
    plot_industry_distributions,
)
from asset_pricing.modeling.tables import write_table


def calculate_descriptive_stats(df):
    """`describe()` of each column plus skewness and kurtosis."""
    desc = df.describe().transpose()
    desc["skew"] = df.skew()
    desc["kurtosis"] = df.kurtosis()
    return desc.transpose()


def main():
    for model_name in MODELS:
        factor_data = load_factors(model_name)
        stats = calculate_descriptive_stats(factor_data)
        write_table(stats, DESCRIPTIVE_FACTORS_TABLE[model_name], index=True)
        if model_name in CORRELATIONS_TABLE:
            corr = factor_data[MODELS[model_name]["factors"]].corr()
            write_table(corr, CORRELATIONS_TABLE[model_name], index=True)

    industry_data = load_industry_data()
    stats = calculate_descriptive_stats(
        industry_data[get_industry_names(industry_data)]
    )
    write_table(stats, DESCRIPTIVE_INDUSTRIES_TABLE, index=True)

    plot_industry_distributions(save_path=FIG_DISTRIBUTION_INDUSTRIES)
    plot_factor_distributions(save_path=FIG_DISTRIBUTION_FACTORS)
    plot_cumulative_log_factor_returns(save_path=FIG_CUMULATIVE_FACTORS)
    plot_cumulative_log_industry_returns(save_path=FIG_CUMULATIVE_INDUSTRIES)


if __name__ == "__main__":
    main()
