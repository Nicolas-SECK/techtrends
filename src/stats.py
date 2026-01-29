from __future__ import annotations

import pandas as pd


def compute_basic_stats(df: pd.DataFrame) -> dict:
    """Return a dict of basic KPIs."""
    return {
        "articles_total": int(len(df)),
        "sources": int(df["source"].nunique()) if "source" in df else 0,
        "authors": int(df["author"].nunique()) if "author" in df else 0,
        "avg_score": float(df["score"].dropna().mean()) if "score" in df else 0.0,
        "avg_comments": float(df["comments"].dropna().mean()) if "comments" in df else 0.0,
    }


def top_sources(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("source")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )


def top_authors(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return (
        df.dropna(subset=["author"])
        .groupby("author")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(n)
    )


def top_tags(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    tags are stored as CSV string (ex: 'ai,webdev').
    """
    if "tags" not in df:
        return pd.DataFrame(columns=["tag", "count"])

    tags = (
        df["tags"]
        .fillna("")
        .astype(str)
        .str.split(",")
        .explode()
        .str.strip()
    )
    tags = tags[tags != ""]
    return (
        tags.value_counts()
        .head(n)
        .reset_index()
        .rename(columns={"index": "tag", "count": "count"})
    )

def articles_per_day(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["day"] = pd.to_datetime(d["published_at"], utc=True, errors="coerce").dt.date
    out = d.dropna(subset=["day"]).groupby(["day", "source"]).size().reset_index(name="count")
    return out.sort_values("day")


def articles_per_hour(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    ts = pd.to_datetime(d["published_at"], utc=True, errors="coerce")
    d["hour"] = ts.dt.hour
    out = d.dropna(subset=["hour"]).groupby(["hour", "source"]).size().reset_index(name="count")
    return out.sort_values("hour")
