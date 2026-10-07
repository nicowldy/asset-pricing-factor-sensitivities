from src.modeling.out_of_sample.pred_config import MODELS, TESTED
from src.modeling.out_of_sample.pred_utils import load_data_with_markers
from src.modeling.out_of_sample.pred_plots import plot_actual_vs_pred, plot_comp_three



def main():
    for m in MODELS:
        df = load_data_with_markers(TESTED[m])
        data = {
            ind: grp.rename(
                columns={"actual_excess": "Actual", "expected_excess": "Expected"}
            )[["Actual", "Expected"]]
            for ind, grp in df.groupby("industry")
        }
        plot_actual_vs_pred(data, m)

    df5 = load_data_with_markers(TESTED["ff5"])
    data3 = {
        ind: grp.rename(
            columns={"actual_excess": "Actual", "expected_excess": "Expected"}
        )[["Actual", "Expected"]]
        for ind, grp in df5[df5["industry"].isin(["Manuf", "Utils"])].groupby("industry")
    }
    plot_comp_three(data3, "ff5", industries=["Manuf", "Utils"])


if __name__ == "__main__":
    main()
