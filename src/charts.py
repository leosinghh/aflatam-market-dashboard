# src/charts.py

import plotly.express as px
import pandas as pd

def line_chart_indicator(df: pd.DataFrame, title: str = ""):
    return px.line(df, x="year", y="value", title=title)

def bar_chart_scores(df_scores: pd.DataFrame):
    return px.bar(
        df_scores.sort_values("score_overall", ascending=False),
        x="country",
        y="score_overall",
        title="Overall Market Attractiveness Score",
    )
