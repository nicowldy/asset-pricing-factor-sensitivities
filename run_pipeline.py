"""Main entry point to execute the asset pricing empirical pipeline.

Enables reproducible execution of data processing, in-sample econometrics,
and out-of-sample predictive evaluations.
"""

from __future__ import annotations

import argparse
import sys
import time


def _stage(title: str, steps) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    for message, step in steps:
        print(f"--> {message}...")
        step()
        print("    [OK]")


def run_data_stage() -> None:
    from asset_pricing.data import processing

    _stage(
        "STAGE 1: DATA",
        [
            (
                "Cleaning the raw files and aligning them to a common sample",
                processing.process_data,
            )
        ],
    )


def run_in_sample_stage() -> None:
    from asset_pricing.modeling.in_sample import (
        decades,
        descriptive,
        diagnostics,
        regression,
        wald,
    )

    _stage(
        "STAGE 2: IN-SAMPLE ANALYSIS",
        [
            ("Descriptive statistics and return plots", descriptive.main),
            ("Full-sample regressions with HAC standard errors", regression.main),
            ("Joint and incremental Wald tests", wald.main),
            ("Assumption diagnostics", diagnostics.main),
            ("Regressions by decade", decades.main),
        ],
    )


def run_out_of_sample_stage() -> None:
    from asset_pricing.modeling.out_of_sample import (
        actual_vs_predicted,
        estimate,
        forecast_tests,
        metrics,
        predict,
    )

    _stage(
        "STAGE 3: OUT-OF-SAMPLE EVALUATION",
        [
            ("Expanding-window estimation of the factor loadings", estimate.main),
            ("Predictions for the month after each window", predict.main),
            ("RMSE and out-of-sample R-squared", metrics.main),
            ("Actual vs. predicted plots", actual_vs_predicted.main),
            ("t-tests on the prediction errors", forecast_tests.main),
        ],
    )


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
        raise


if __name__ == "__main__":
    main()
