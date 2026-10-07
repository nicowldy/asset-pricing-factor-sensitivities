"""Main entry point to execute the asset pricing empirical pipeline.

Enables reproducible execution of data processing, in-sample econometrics,
and out-of-sample predictive evaluations.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path


def run_data_stage() -> None:
    """Run data extraction and preprocessing."""
    print("\n" + "=" * 60)
    print("STAGE 1: DATA EXTRACTION & PREPROCESSING")
    print("=" * 60)

    from src.data.data_capm import extract_market_factor_data
    from src.data.data_processing import process_data

    print("--> Extracting CAPM market factor data from Fama-French 3-Factor raw source...")
    extract_market_factor_data()
    print("    [OK] CAPM raw extraction completed.")

    print("--> Aligning sample windows, cleaning, and exporting processed datasets...")
    process_data()
    print("    [OK] Data processing completed.")


def run_in_sample_stage() -> None:
    """Run in-sample empirical asset pricing regressions and diagnostic tests."""
    print("\n" + "=" * 60)
    print("STAGE 2: IN-SAMPLE ECONOMETRIC ANALYSIS")
    print("=" * 60)

    from src.modeling.in_sample.expl_descript import run_all_analyses as run_descript
    from src.modeling.in_sample.expl_regress import run_analysis as run_regress
    from src.modeling.in_sample.expl_jointwald import main as run_jointwald
    from src.modeling.in_sample.expl_incrwald import main as run_incrwald
    from src.modeling.in_sample.expl_assumptions import main as run_assumptions
    from src.modeling.in_sample.expl_bydecs import main as run_bydecs

    print("--> Computing descriptive statistics and cumulative return plots...")
    run_descript(save_plots=True)
    print("    [OK] Descriptive statistics & plots generated.")

    print("--> Running full-sample time-series regressions (HAC standard errors)...")
    run_regress(save_outputs=True)
    print("    [OK] In-sample regressions & R-squared comparison generated.")

    print("--> Performing Joint Wald tests for factor significance...")
    run_jointwald()
    print("    [OK] Joint Wald tests completed.")

    print("--> Performing Incremental Wald tests (CAPM vs FF3, FF3 vs FF5)...")
    run_incrwald()
    print("    [OK] Incremental Wald tests completed.")

    print("--> Evaluating econometric regression assumptions & diagnostics...")
    run_assumptions(save_to_csv=True)
    print("    [OK] Assumption diagnostics completed.")

    print("--> Evaluating decade-by-decade parameter and explanatory power stability...")
    run_bydecs()
    print("    [OK] Decade-by-decade analysis completed.")


def run_out_of_sample_stage() -> None:
    """Run out-of-sample expanding window predictive modeling and evaluation."""
    print("\n" + "=" * 60)
    print("STAGE 3: OUT-OF-SAMPLE PREDICTIVE EVALUATION")
    print("=" * 60)

    from src.modeling.out_of_sample.pred_train import main as run_train
    from src.modeling.out_of_sample.pred_test import main as run_test
    from src.modeling.out_of_sample.pred_metrics import main as run_metrics
    from src.modeling.out_of_sample.pred_actpred import main as run_actpred
    from src.modeling.out_of_sample.pred_ttest import main as run_ttest
    from src.modeling.out_of_sample.pred_pairttest import main as run_pairttest

    print("--> Training predictive models via expanding window OLS...")
    run_train()
    print("    [OK] Model training completed.")

    print("--> Generating 1-step-ahead out-of-sample predictions...")
    run_test()
    print("    [OK] Prediction generation completed.")

    print("--> Calculating prediction accuracy metrics (RMSE, out-of-sample R²)...")
    run_metrics()
    print("    [OK] Prediction metrics and comparison plots completed.")

    print("--> Generating actual vs. predicted visualization charts...")
    run_actpred()
    print("    [OK] Prediction plots completed.")

    print("--> Running Diebold-Mariano / t-tests on forecast errors...")
    run_ttest()
    print("    [OK] Forecast error t-tests completed.")

    print("--> Performing paired t-tests comparing predictive performance...")
    run_pairttest()
    print("    [OK] Paired t-tests completed.")


def main() -> None:
    """Parse CLI arguments and dispatch pipeline execution."""
    parser = argparse.ArgumentParser(
        description="Empirical Asset Pricing Factor Sensitivities Pipeline",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Execute the full end-to-end pipeline (Data, In-Sample, Out-Of-Sample)",
    )
    parser.add_argument(
        "--data",
        action="store_true",
        help="Run data preprocessing only",
    )
    parser.add_argument(
        "--in-sample",
        action="store_true",
        dest="in_sample",
        help="Run in-sample econometric regressions and statistical tests",
    )
    parser.add_argument(
        "--out-of-sample",
        action="store_true",
        dest="out_of_sample",
        help="Run out-of-sample training, forecasting, and evaluation",
    )

    args = parser.parse_args()

    # Default to running all stages if no flag is specified
    if not (args.all or args.data or args.in_sample or args.out_of_sample):
        args.all = True

    t0 = time.time()
    print("\n" + "#" * 60)
    print("  EMPIRICAL ASSET PRICING RESEARCH PIPELINE")
    print("  Evaluating CAPM, Fama-French 3-Factor & 5-Factor Models")
    print("#" * 60)

    try:
        if args.all or args.data:
            run_data_stage()
        if args.all or args.in_sample:
            run_in_sample_stage()
        if args.all or args.out_of_sample:
            run_out_of_sample_stage()

        elapsed = time.time() - t0
        print("\n" + "=" * 60)
        print(f" PIPELINE EXECUTION SUCCESSFUL (Elapsed: {elapsed:.2f}s)")
        print(" All tables and figures are updated in `reports/`.")
        print("=" * 60 + "\n")
    except Exception as exc:
        print(f"\n[ERROR] Pipeline failed with error: {exc}", file=sys.stderr)
        raise exc


if __name__ == "__main__":
    main()
