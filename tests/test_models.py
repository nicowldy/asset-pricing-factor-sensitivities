"""Unit and integration tests for asset pricing models and econometric tests."""

import pytest

from asset_pricing.config import MODELS
from asset_pricing.data.loaders import (
    calculate_excess_returns,
    load_factors,
    load_industry_data,
)
from asset_pricing.modeling.in_sample.regression import run_regression
from asset_pricing.modeling.in_sample.wald import wald_test


@pytest.fixture
def sample_factor_and_excess_industry_data():
    """Fixture providing clean factor and excess return industry datasets."""
    fact_df = load_factors("ff3")
    ind_df = load_industry_data()
    # Strip any column whitespace in industries
    ind_df.columns = [c.strip() for c in ind_df.columns]
    excess_df = calculate_excess_returns(ind_df, fact_df)
    return fact_df, excess_df


def test_model_configurations():
    """Verify that model specifications have valid factors and definitions."""
    assert "capm" in MODELS
    assert "ff3" in MODELS
    assert "ff5" in MODELS

    assert MODELS["capm"]["factors"] == ["MKT"]
    assert MODELS["ff3"]["factors"] == ["MKT", "SMB", "HML"]
    assert MODELS["ff5"]["factors"] == ["MKT", "SMB", "HML", "RMW", "CMA"]


def test_ols_regression_with_hac(sample_factor_and_excess_industry_data):
    """Test running OLS regression with Newey-West HAC standard errors."""
    fact_df, excess_df = sample_factor_and_excess_industry_data
    factors = ["MKT", "SMB", "HML"]
    target_industry = "Manuf"

    results = run_regression(
        fact_df, excess_df, factors, target_industry, cov_type="HAC"
    )

    assert results is not None
    assert "const" in results.params
    for f in factors:
        assert f in results.params
    # R-squared in reasonable empirical range
    assert 0.5 < results.rsquared < 1.0
    # Manufacturing market beta should be close to 1
    assert 0.7 < results.params["MKT"] < 1.3


def test_joint_wald_test(sample_factor_and_excess_industry_data):
    """Test computation of Wald test statistic for joint significance."""
    fact_df, excess_df = sample_factor_and_excess_industry_data
    factors = ["MKT", "SMB", "HML"]
    target_industry = "Manuf"

    results = run_regression(fact_df, excess_df, factors, target_industry)
    wald_stat, p_val = wald_test(results, factors)

    assert wald_stat > 0
    assert 0.0 <= p_val <= 1.0
    # Market & size/value factors are overwhelmingly jointly significant in Manufacturing
    assert p_val < 0.01
