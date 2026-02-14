"""Runtime data fetching with Streamlit caching for Opportunity Insights datasets."""

import os

import pandas as pd
import streamlit as st

from src.config import DATA_URLS, DATASETS, NATIONAL_URLS


def _build_date_col(df, date_cols):
    """Build a datetime column from year/month/day component columns."""
    df = df.copy()
    year = df["year"].astype(int)
    month = df["month"].astype(int)
    day_col = [c for c in date_cols if c not in ("year", "month")][0]
    day = df[day_col].astype(int)
    df["date"] = pd.to_datetime(
        year.astype(str) + "-" + month.astype(str) + "-" + day.astype(str),
        format="%Y-%m-%d",
        errors="coerce",
    )
    return df


def _load_county_coords():
    """Load county lat/lng coordinates from local CSV."""
    path = os.path.join(os.path.dirname(__file__), "..", "data", "us_county_latlng.csv")
    coords = pd.read_csv(path)
    coords["countyfips"] = coords["countyfips"].astype(int)
    return coords


@st.cache_data(ttl="24h", show_spinner="Fetching data...")
def get_chart_data(key):
    """Fetch full time-series data for a dataset, merged with county names.

    Returns a DataFrame with columns: date, countyfips, county_name, state,
    location, + metric columns.
    """
    cfg = DATASETS[key]
    url = DATA_URLS[key]

    df = pd.read_csv(url, na_values=".")
    df = _build_date_col(df, cfg["date_cols"])
    df = df.dropna(subset=["date"])

    for col in cfg["drop_cols"]:
        if col in df.columns:
            df = df.drop(columns=[col])

    for col in cfg["date_cols"]:
        if col in df.columns:
            df = df.drop(columns=[col])

    coords = _load_county_coords()
    df["countyfips"] = df["countyfips"].astype(int)
    df = df.merge(
        coords[["countyfips", "county_name", "state"]],
        on="countyfips",
        how="left",
    )
    df = df.dropna(subset=["county_name"])
    df["location"] = df["county_name"] + ", " + df["state"]

    return df.sort_values("date").reset_index(drop=True)


@st.cache_data(ttl="24h", show_spinner="Fetching map data...")
def get_map_data(key):
    """Get the latest value per county for map rendering.

    Returns ~3,200 rows with: countyfips, county_name, state, lat, lng,
    location, date, + latest metric values.
    """
    cfg = DATASETS[key]
    url = DATA_URLS[key]

    df = pd.read_csv(url, na_values=".")
    df = _build_date_col(df, cfg["date_cols"])
    df = df.dropna(subset=["date"])

    for col in cfg["drop_cols"]:
        if col in df.columns:
            df = df.drop(columns=[col])
    for col in cfg["date_cols"]:
        if col in df.columns:
            df = df.drop(columns=[col])

    latest = (
        df.sort_values("date")
        .groupby("countyfips")
        .last()
        .reset_index()
    )

    coords = _load_county_coords()
    latest["countyfips"] = latest["countyfips"].astype(int)
    latest = latest.merge(coords, on="countyfips", how="inner")
    latest["location"] = latest["county_name"] + ", " + latest["state"]

    return latest


@st.cache_data(ttl="24h", show_spinner="Fetching national data...")
def get_national_data(key):
    """Fetch national-level data for landing page summaries."""
    if key not in NATIONAL_URLS:
        return None

    cfg = DATASETS[key]
    url = NATIONAL_URLS[key]

    df = pd.read_csv(url, na_values=".")
    df = _build_date_col(df, cfg["date_cols"])
    df = df.dropna(subset=["date"])

    for col in cfg["date_cols"]:
        if col in df.columns:
            df = df.drop(columns=[col])
    for col in cfg.get("drop_cols", []):
        if col in df.columns:
            df = df.drop(columns=[col])

    # Drop non-metric columns that may appear at national level
    keep_cols = ["date"] + list(cfg["metrics"].keys())
    df = df[[c for c in keep_cols if c in df.columns]]

    return df.sort_values("date").reset_index(drop=True)
