import os
import pandas as pd
try:
    from src.modeling.in_sample.expl_utils import (
        run_all_regressions,
        get_industry_names,
        load_industry_data,
        add_average_row,
        perform_hac_wald_test,
        load_factors,
        calculate_excess_returns,
        get_models,
    )
    from src.modeling.in_sample.expl_config import TABLES_DIR
    from src.modeling.in_sample.expl_tables import write_incrwald_results
except ModuleNotFoundError:
    try:
        from modeling.in_sample.expl_utils import (
            run_all_regressions,
            get_industry_names,
            load_industry_data,
            add_average_row,
            perform_hac_wald_test,
            load_factors,
            calculate_excess_returns,
            get_models,
        )
        from modeling.in_sample.expl_config import TABLES_DIR
        from modeling.in_sample.expl_tables import write_incrwald_results
    except ModuleNotFoundError:
        from expl_utils import (
            run_all_regressions,
            get_industry_names,
            load_industry_data,
            add_average_row,
            perform_hac_wald_test,
            load_factors,
            calculate_excess_returns,
            get_models,
        )
        from expl_config import TABLES_DIR
        from expl_tables import write_incrwald_results



def main():
    os.makedirs(TABLES_DIR, exist_ok=True)

    all_results = run_all_regressions()
    industry_data = load_industry_data()
    industry_names = get_industry_names(industry_data)

    models = get_models()
    factor_data_capm = load_factors("capm")
    factor_data_ff3 = load_factors("ff3")
    factor_data_ff5 = load_factors("ff5")
    industry_data_excess = calculate_excess_returns(industry_data, factor_data_capm)

    results_ff3_ff5 = []
    results_capm_ff3 = []

    for industry in industry_names:
        capm_res = all_results["capm"][industry]
        ff3_res = all_results["ff3"][industry]
        ff5_res = all_results["ff5"][industry]

        wald3f5_stat, p3f5 = perform_hac_wald_test(
            factor_data_ff5,
            industry_data_excess,
            industry,
            models["ff3"]["factors"],
            models["ff5"]["factors"],
        )
        delta3f5 = ff5_res["adj_r_squared"] - ff3_res["adj_r_squared"]
        results_ff3_ff5.append(
            {
                "industry": industry,
                "adj_r2_ff3": ff3_res["adj_r_squared"],
                "adj_r2_ff5": ff5_res["adj_r_squared"],
                "delta_adj_r2": delta3f5,
                "wald_stat": wald3f5_stat,
                "p_value": p3f5,
            }
        )

        waldcf3_stat, pcf3 = perform_hac_wald_test(
            factor_data_ff3,
            industry_data_excess,
            industry,
            models["capm"]["factors"],
            models["ff3"]["factors"],
        )
        deltacf3 = ff3_res["adj_r_squared"] - capm_res["adj_r_squared"]
        results_capm_ff3.append(
            {
                "industry": industry,
                "adj_r2_capm": capm_res["adj_r_squared"],
                "adj_r2_ff3": ff3_res["adj_r_squared"],
                "delta_adj_r2": deltacf3,
                "wald_stat": waldcf3_stat,
                "p_value": pcf3,
            }
        )

    df_ff3_ff5 = add_average_row(pd.DataFrame(results_ff3_ff5))
    df_capm_ff3 = add_average_row(pd.DataFrame(results_capm_ff3))

    write_incrwald_results(df_ff3_ff5, df_capm_ff3)


if __name__ == "__main__":
    main()
