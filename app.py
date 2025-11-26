# app.py

import streamlit as st
import pandas as pd

from src.config import AFRICA_COUNTRIES, LATAM_COUNTRIES, WORLD_BANK_INDICATORS
from src.data_fetchers import fetch_indicator
from src.data_processing import compute_country_scores
from src.charts import line_chart_indicator, bar_chart_scores

st.set_page_config(
    page_title="Africa & LATAM Market Dashboard",
    layout="wide"
)

st.title("🌍 Africa & LATAM Market Data Dashboard")
st.caption("Non-AI, data-driven view of emerging markets using World Bank data.")

region = st.sidebar.selectbox("Region", ["Africa", "Latin America"])
if region == "Africa":
    countries = AFRICA_COUNTRIES
else:
    countries = LATAM_COUNTRIES

selected_countries = st.sidebar.multiselect("Select countries", countries, default=countries[:3])

indicator_label = st.sidebar.selectbox(
    "Indicator",
    list(WORLD_BANK_INDICATORS.keys())
)
indicator_code = WORLD_BANK_INDICATORS[indicator_label]

st.sidebar.markdown("---")
st.sidebar.write("Showing data since 2000.")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"{indicator_label} over time")
    for country in selected_countries:
        df = fetch_indicator(country, indicator_code)
        if df.empty:
            st.warning(f"No data for {country}")
            continue
        fig = line_chart_indicator(df, title=f"{country} – {indicator_label}")
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Market Attractiveness Snapshot (Experimental)")

    # Example: build a small latest-year scoring table for selected countries
    snapshot_rows = []
    for country in selected_countries:
        try:
            gdp_growth = fetch_indicator(country, WORLD_BANK_INDICATORS["GDP growth (annual %)"]).dropna().tail(1)
            gdp_pc = fetch_indicator(country, WORLD_BANK_INDICATORS["GDP per capita (current US$)"]).dropna().tail(1)
            inflation = fetch_indicator(country, WORLD_BANK_INDICATORS["Inflation, consumer prices (annual %)"]).dropna().tail(1)
            fdi = fetch_indicator(country, WORLD_BANK_INDICATORS["Foreign direct investment, net inflows (BoP, current US$)"]).dropna().tail(1)
            unemp = fetch_indicator(country, WORLD_BANK_INDICATORS["Unemployment, total (% of total labor force)"]).dropna().tail(1)
            pop = fetch_indicator(country, WORLD_BANK_INDICATORS["Population, total"]).dropna().tail(1)

            # Align by latest available year for simplicity
            latest_year = int(
                min(
                    gdp_growth["year"].max(),
                    gdp_pc["year"].max(),
                    inflation["year"].max(),
                    fdi["year"].max(),
                    unemp["year"].max(),
                    pop["year"].max(),
                )
            )

            snapshot_rows.append({
                "country": country,
                "year": latest_year,
                "gdp_growth": float(gdp_growth[gdp_growth["year"] == latest_year]["value"]),
                "gdp_per_capita": float(gdp_pc[gdp_pc["year"] == latest_year]["value"]),
                "inflation": float(inflation[inflation["year"] == latest_year]["value"]),
                "fdi": float(fdi[fdi["year"] == latest_year]["value"]),
                "unemployment": float(unemp[unemp["year"] == latest_year]["value"]),
                "population": float(pop[pop["year"] == latest_year]["value"]),
            })
        except Exception:
            st.warning(f"Insufficient data to compute snapshot for {country}")

    if snapshot_rows:
        df_snapshot = pd.DataFrame(snapshot_rows)
        df_scores = compute_country_scores(df_snapshot)
        st.dataframe(df_scores[["country", "year", "score_overall"]])
        fig_scores = bar_chart_scores(df_scores)
        st.plotly_chart(fig_scores, use_container_width=True)
    else:
        st.info("Select countries with sufficient data to see the scoring summary.")
