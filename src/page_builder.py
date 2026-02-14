"""Generic page rendering function for all dataset pages (DRY)."""

import streamlit as st

from src.config import DATASETS
from src.data_loader import get_chart_data, get_map_data
from src.maps import build_county_map
from src.charts import build_time_series


def render_dataset_page(key):
    """Render a complete dataset page with map and time-series chart.

    Args:
        key: Dataset key from DATASETS config (e.g., "spending").
    """
    cfg = DATASETS[key]
    metric_keys = list(cfg["metrics"].keys())

    st.title(f"{cfg['icon']} {cfg['title']}")
    st.markdown(cfg["description"])
    st.caption(f"Source: {cfg['source']} | Baseline: {cfg['baseline']}")

    st.divider()

    # --- Map section ---
    st.subheader("County Map")

    map_metric = st.selectbox(
        "Select metric for map",
        options=metric_keys,
        format_func=lambda x: cfg["metrics"][x],
        key=f"{key}_map_metric",
    )

    map_data = get_map_data(key)
    fig_map = build_county_map(map_data, key, map_metric)

    if fig_map:
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("No data available for the selected metric.")

    if "date" in map_data.columns and not map_data.empty:
        latest_date = map_data["date"].max()
        st.caption(
            f"Showing latest available data as of {latest_date.strftime('%B %d, %Y')}"
        )

    st.divider()

    # --- Time-series section ---
    st.subheader("County Time Series")

    chart_data = get_chart_data(key)

    available_counties = sorted(chart_data["location"].dropna().unique())

    col1, col2 = st.columns([2, 1])
    with col1:
        default_count = min(3, len(available_counties))
        selected_counties = st.multiselect(
            "Select counties to compare",
            options=available_counties,
            default=available_counties[:default_count],
            max_selections=8,
            key=f"{key}_counties",
        )
    with col2:
        chart_metric = st.selectbox(
            "Select metric for chart",
            options=metric_keys,
            format_func=lambda x: cfg["metrics"][x],
            key=f"{key}_chart_metric",
        )

    if selected_counties:
        fig_chart = build_time_series(chart_data, key, chart_metric, selected_counties)
        if fig_chart:
            st.plotly_chart(fig_chart, use_container_width=True)
        else:
            st.warning("No data available for the selected counties and metric.")
    else:
        st.info("Select at least one county to view the time series.")
