"""Unit and integration tests for data loading, processing, and integrity."""

import pandas as pd

from asset_pricing.config import FACTORS_PROCESSED, INDUSTRY_PROCESSED
from asset_pricing.data.storage import read_marked_csv


def test_processed_files_exist():
    """Verify that all processed data files exist in data/processed/."""
    expected_files = [*FACTORS_PROCESSED.values(), INDUSTRY_PROCESSED]
    for file_path in expected_files:
        assert file_path.exists(), f"Processed data file missing: {file_path}"
        assert file_path.stat().st_size > 0, (
            f"Processed data file is empty: {file_path}"
        )


def test_processed_data_loading_and_markers():
    """Test that read_marked_csv correctly strips comments and parses dates."""
    df_capm = read_marked_csv(FACTORS_PROCESSED["capm"])
    assert not df_capm.empty
    assert "Date" in df_capm.columns
    assert "MKT" in df_capm.columns
    assert "RF" in df_capm.columns
    assert pd.api.types.is_datetime64_any_dtype(df_capm["Date"])


def test_industry_sectors_present():
    """Verify that all 12 Kenneth French industry portfolios are present."""
    expected_sectors = [
        "NoDur",
        "Durbl",
        "Manuf",
        "Enrgy",
        "Chems",
        "BusEq",
        "Telcm",
        "Utils",
        "Shops",
        "Hlth",
        "Money",
        "Other",
    ]
    df_ind = read_marked_csv(INDUSTRY_PROCESSED)
    assert not df_ind.empty
    # Strip any trailing whitespace from Kenneth French column names
    cols = [c.strip() for c in df_ind.columns]
    for sector in expected_sectors:
        assert sector in cols, f"Industry sector '{sector}' not found in processed data"


def test_date_alignment_across_processed_datasets():
    """Verify that date ranges are identical across factor and industry datasets."""
    datasets = {
        "capm": read_marked_csv(FACTORS_PROCESSED["capm"]),
        "ff3": read_marked_csv(FACTORS_PROCESSED["ff3"]),
        "ff5": read_marked_csv(FACTORS_PROCESSED["ff5"]),
        "ind": read_marked_csv(INDUSTRY_PROCESSED),
    }

    reference_dates = datasets["capm"]["Date"].tolist()
    assert len(reference_dates) > 600, (
        "Sample size should be over 50 years of monthly data"
    )

    for name, df in datasets.items():
        assert len(df) == len(reference_dates), f"{name} length mismatch"
        assert df["Date"].tolist() == reference_dates, (
            f"{name} dates do not align with reference"
        )
        # Check no missing values
        assert df.isna().sum().sum() == 0, f"{name} contains NaN values"
