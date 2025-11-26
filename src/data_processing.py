# src/data_processing.py

import pandas as pd

def normalize_series(s: pd.Series, reverse: bool = False) -> pd.Series:
    """Min-max normalize a series to [0,1]. If reverse=True, lower is better."""
    s = s.astype(float)
    min_val, max_val = s.min(), s.max()
    if max_val == min_val:
        return pd.Series([0.5] * len(s), index=s.index)
    norm = (s - min_val) / (max_val - min_val)
    return 1 - norm if reverse else norm


def compute_country_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    df columns expected:
      country, gdp_growth, gdp_per_capita, inflation, fdi, unemployment, population
      (e.g. latest-year snapshot for each country)
    """
    result = df.copy()

    result["score_growth"] = normalize_series(result["gdp_growth"])
    result["score_income"] = normalize_series(result["gdp_per_capita"])
    result["score_stability"] = (
        normalize_series(result["inflation"], reverse=True) +
        normalize_series(result["unemployment"], reverse=True)
    ) / 2
    result["score_market_size"] = normalize_series(result["population"])

    # You can tweak weights based on your POV
    result["score_overall"] = (
        0.3 * result["score_growth"] +
        0.3 * result["score_income"] +
        0.2 * result["score_stability"] +
        0.2 * result["score_market_size"]
    )

    return result
