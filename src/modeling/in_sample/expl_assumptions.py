import pandas as pd
import statsmodels.api as sm
from src.modeling.in_sample.expl_tables import write_assumption_results
from src.modeling.in_sample.expl_config import get_resids_path
from src.modeling.in_sample import expl_utils
from src.modeling.in_sample.expl_plots import plot_residuals_fitted_grid



def main(save_to_csv=True, cov_type="HAC"):
    models = expl_utils.get_models()
    industry_data = expl_utils.load_industry_data()
    industries = expl_utils.get_industry_names(industry_data)
    all_results = []

    for model_name, model_info in models.items():
        factor_data = expl_utils.load_factors(model_name)
        industry_data_with_excess = expl_utils.calculate_excess_returns(
            industry_data, factor_data
        )
        X_with_const = sm.add_constant(factor_data[model_info["factors"]])
        multi_test = expl_utils.test_multicollinearity(X_with_const)
        vif_values = multi_test["vif_data"].set_index("Variable")["VIF"].to_dict()
        reg_results = {}

        for industry in industries:
            try:
                results = expl_utils.run_regression(
                    factor_data,
                    industry_data_with_excess,
                    model_info["factors"],
                    industry,
                    cov_type=cov_type,
                )
                reg_results[industry] = expl_utils.get_regression_parameters(results)
                excess_returns = industry_data_with_excess[f"{industry}_Excess"]
                lin_test = expl_utils.test_linearity(results)
                ind_test = expl_utils.test_independence(results)
                homo_test = expl_utils.test_homoskedasticity(results)
                stat_test = expl_utils.test_stationarity(excess_returns)

                tests_passed = (
                    lin_test["passed"]
                    + ind_test["dw_passed"]
                    + homo_test["passed"]
                    + multi_test["passed"]
                    + stat_test["passed"]
                )
                tests_total = 5

                result_dict = {
                    "model": model_name,
                    "industry": industry,
                    "cov_type": cov_type,
                    "linearity_correlation": lin_test["correlation"],
                    "linearity_passed": lin_test["passed"],
                    "dw_stat": ind_test["dw_stat"],
                    "autocorrelation_passed": ind_test["dw_passed"],
                    "bp_stat": homo_test["bp_stat"],
                    "bp_pvalue": homo_test["bp_pvalue"],
                    "homoskedasticity_passed": homo_test["passed"],
                    "max_vif": multi_test["max_vif"],
                    "multicollinearity_passed": multi_test["passed"],
                    "adf_stat": stat_test["adf_stat"],
                    "adf_pvalue": stat_test["adf_pvalue"],
                    "stationarity_passed": stat_test["passed"],
                    "tests_passed": tests_passed,
                    "tests_failed": tests_total - tests_passed,
                    "all_tests_passed": tests_passed == tests_total,
                }

                for factor, vif in vif_values.items():
                    if factor != "const":
                        result_dict[f"vif_{factor}"] = vif

                all_results.append(result_dict)

            except Exception as e:
                all_results.append(
                    {
                        "model": model_name,
                        "industry": industry,
                        "cov_type": cov_type,
                        "error": str(e),
                    }
                )

        plot_residuals_fitted_grid(
            reg_results, save_path=get_resids_path(model_name)
        )

    if save_to_csv and all_results:
        results_df = pd.DataFrame(all_results)
        write_assumption_results(results_df)
        return results_df

    return pd.DataFrame(all_results) if all_results else None


if __name__ == "__main__":
    main(save_to_csv=True, cov_type="HAC")
