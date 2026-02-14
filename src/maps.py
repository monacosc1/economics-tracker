"""Plotly scatter_mapbox map builders for county-level data."""

import plotly.express as px

from src.config import DATASETS


def build_county_map(map_data, key, metric):
    """Build a Plotly scatter_mapbox showing county-level data.

    Args:
        map_data: DataFrame from get_map_data() with lat, lng, metric columns.
        key: Dataset key (e.g., "spending").
        metric: Column name of the metric to display.

    Returns:
        Plotly figure, or None if no data.
    """
    cfg = DATASETS[key]
    metric_label = cfg["metrics"][metric]

    plot_df = map_data.dropna(subset=[metric]).copy()
    if plot_df.empty:
        return None

    if cfg["value_format"] == "pct_change":
        plot_df["display"] = (plot_df[metric] * 100).round(1).astype(str) + "%"
        color_midpoint = 0
        color_scale = "RdYlGn"
    elif metric == "initclaims_count_regular":
        plot_df["display"] = plot_df[metric].round(0).astype(int).astype(str)
        color_midpoint = None
        color_scale = "YlOrRd"
    else:
        plot_df["display"] = plot_df[metric].round(2).astype(str)
        color_midpoint = None
        color_scale = "YlOrRd"

    fig = px.scatter_mapbox(
        plot_df,
        lat="lat",
        lon="lng",
        color=metric,
        hover_name="location",
        hover_data={
            "lat": False,
            "lng": False,
            metric: ":.4f",
            "display": True,
        },
        color_continuous_scale=color_scale,
        color_continuous_midpoint=color_midpoint,
        zoom=3,
        center={"lat": 39.8, "lon": -98.5},
        mapbox_style="carto-positron",
        title=f"{metric_label} by County",
        labels={"display": metric_label},
    )

    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        height=500,
        coloraxis_colorbar_title=metric_label,
    )
    fig.update_traces(marker={"size": 5, "opacity": 0.7})

    return fig
