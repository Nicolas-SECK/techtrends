from __future__ import annotations
import pandas as pd
import plotly.express as px


def plot_articles_per_day(per_day: pd.DataFrame):
    fig = px.line(
        per_day,
        x="day",
        y="count",
        color="source",
        markers=True,
        title="Articles par jour (par source)",
    )
    fig.update_layout(xaxis_title="Jour", yaxis_title="Nombre d’articles")
    return fig


def plot_articles_per_hour(per_hour: pd.DataFrame):
    fig = px.bar(
        per_hour,
        x="hour",
        y="count",
        color="source",
        barmode="group",
        title="Articles par heure (par source)",
    )
    fig.update_layout(xaxis_title="Heure", yaxis_title="Nombre d’articles")
    return fig
