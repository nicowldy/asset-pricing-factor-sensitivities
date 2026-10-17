"""Load the processed factor and industry returns, indexed by date."""

from asset_pricing.config import FACTORS_PROCESSED, INDUSTRY_PROCESSED
from asset_pricing.data.storage import read_marked_csv


def load_industry_data():
    return read_marked_csv(INDUSTRY_PROCESSED).set_index("Date")


def load_factors(model_name):
    return read_marked_csv(FACTORS_PROCESSED[model_name]).set_index("Date")


def get_industry_names(industry_data):
    return [
        col
        for col in industry_data.columns
        if col != "Date" and not col.endswith("_Excess")
    ]


def calculate_excess_returns(industry_data, factor_data):
    """Add an `<industry>_Excess` column with the return minus the risk-free rate."""
    result = industry_data.copy()
    for industry in get_industry_names(industry_data):
        result[f"{industry}_Excess"] = industry_data[industry] - factor_data["RF"]
    return result
