aflatam-market-dashboard/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── app.py                      # main Streamlit app
├── src/
│   ├── __init__.py
│   ├── config.py               # regions, indicators, scoring weights
│   ├── data_fetchers.py        # API calls (World Bank, etc.)
│   ├── data_processing.py      # cleaning, normalization, scoring
│   ├── charts.py               # plotting helpers
│   └── utils.py                # small helpers (caching, etc.)
├── data/
│   ├── raw/                    # optional cached JSON/CSV
│   └── processed/              # optional precomputed scores
├── tests/
│   ├── __init__.py
│   └── test_scoring.py         # unit tests for your scoring
└── .streamlit/
    └── config.toml             # theme controls
