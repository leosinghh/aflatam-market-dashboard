# src/data_fetchers.py

import requests
import pandas as pd
from functools import lru_cache
from typing import List

BASE_URL = "https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json&per_page=100"

# You may want a small mapping from country name -> ISO2 code
COUNTRY_CODE_MAP = {
    "Ghana": "GH",
    "Nigeria": "NG",
    "Kenya": "KE",
    "South Africa": "ZA",
    "Egypt": "EG",
    "Côte d'Ivoire": "CI",
    "Rwanda": "RW",
    "Ethiopia": "ET",
    "Mexico": "MX",
    "Brazil": "BR",
    "Colombia": "CO",
    "Chile": "CL",
    "Peru": "PE",
    "Argentina": "AR",
    "Costa Rica": "CR",
}

@lru_cache(maxsize=128)
def fetch_indicator(country_name: str, indicator_code: str, start_year: int = 2000) -> pd.DataFrame:
    """Fetch a single indicator for a country from the World Bank."""
    country_code = COUNTRY_CODE_MAP[country_name]
    url = BASE_URL.format(country_code=country_code, indicator=indicator_code)
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    data = resp.json()[1]  # [0] is metadata, [1] is data list
    records = []
    for item in data:
        year = int(item["date"])
        if year < start_year:
            continue
        value = item["value"]
        records.append({"year": year, "value": value})

    df = pd.DataFrame(records)
    return df.sort_values("year")
