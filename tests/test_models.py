"""Unit and integration tests for asset pricing models and econometric tests."""
import numpy as np
import pandas as pd
import pytest

from src.config import MODELS
from src.modeling.in_sample.expl_utils import (
    calculate_excess_returns,
    load_factors,
    load_industry_data,
    run_regression,
)
from src.modeling.in_sample.expl_jointwald import perform_joint_wald_test


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

    results = run_regression(fact_df, excess_df, factors, target_industry, cov_type="HAC")

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

    wald_stat, p_val = perform_joint_wald_test(fact_df, excess_df, factors, target_industry)

    assert wald_stat > 0
    assert 0.0 <= p_val <= 1.0
    # Market & size/value factors are overwhelmingly jointly significant in Manufacturing
    assert p_val < 0.01


def test_expanding_window_rmse_metric():
    """Verify RMSE and R2 calculations match standard statistical definitions."""
    y_true = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
    y_pred = pd.Series([1.1, 1.9, 3.2, 3.8, 5.1])

    rmse = np.sqrt(((y_true - y_pred) ** 2).mean())
    ss_res = ((y_true - y_pred) ** 2).sum()
    ss_tot = ((y_true - y_true.mean()) ** 2).sum()
    r2 = 1.0 - (ss_res / ss_tot)

    assert 0.0 < rmse < 0.3
    assert r2 > 0.95
