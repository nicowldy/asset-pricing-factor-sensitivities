import pandas as pd

from asset_pricing.modeling.in_sample.expl_tables import write_jointwald_results
from asset_pricing.modeling.in_sample.expl_utils import (
    add_average_row,
    calculate_excess_returns,
    get_industry_names,
    get_models,
    load_factors,
    load_industry_data,
    run_regression,
    wald_test,
)


def main():
    industry_data = load_industry_data()
    industry_names = get_industry_names(industry_data)
    industry_data_excess = calculate_excess_returns(industry_data, load_factors("capm"))

    for model_name, model_info in get_models().items():
        factors = model_info["factors"]
        factor_data = load_factors(model_name)
        rows = []
        for industry in industry_names:
            results = run_regression(
                factor_data, industry_data_excess, factors, industry, cov_type="HAC"
            )
            wald_stat, p_value = wald_test(results, factors)
            rows.append(
                {
                    "industry": industry,
                    "adj_r2": results.rsquared_adj,
                    "wald_stat": wald_stat,
                    "p_value": p_value,
                }
            )
        write_jointwald_results(model_name, add_average_row(pd.DataFrame(rows)))


if __name__ == "__main__":
    main()
