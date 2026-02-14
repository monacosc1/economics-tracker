"""Plotly time-series chart builders."""

import plotly.express as px
import plotly.graph_objects as go

from src.config import DATASETS, COLORS


def build_time_series(chart_data, key, metric, selected_counties):
    """Build a Plotly time-series line chart for selected counties.

    Args:
        chart_data: DataFrame from get_chart_data().
        key: Dataset key.
        metric: Column name of metric to plot.
        selected_counties: List of "County, State" strings.

    Returns:
        Plotly figure, or None if no data.
    """
    cfg = DATASETS[key]
    metric_label = cfg["metrics"][metric]

    filtered = chart_data[chart_data["location"].isin(selected_counties)].copy()
    filtered = filtered.dropna(subset=[metric])

    if filtered.empty:
        return None

    fig = px.line(
        filtered,
        x="date",
        y=metric,
        color="location",
        title=f"{metric_label} Over Time",
        labels={metric: metric_label, "date": "Date", "location": "County"},
        color_discrete_sequence=COLORS["chart_colors"],
    )

    if cfg["value_format"] == "pct_change":
        fig.add_hline(
            y=0,
            line_dash="dash",
            line_color=COLORS["neutral"],
            annotation_text="Jan 2020 Baseline",
            annotation_position="bottom right",
        )

    fig.update_layout(
        margin={"r": 20, "t": 40, "l": 20, "b": 20},
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3),
        hovermode="x unified",
    )

    return fig


def build_national_chart(national_data, key, metric):
    """Build a national-level time-series chart for the landing page."""
    cfg = DATASETS[key]
    metric_label = cfg["metrics"][metric]

    plot_df = national_data.dropna(subset=[metric]).copy()
    if plot_df.empty:
        return None

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=plot_df["date"],
            y=plot_df[metric],
            mode="lines",
            name=metric_label,
            line=dict(color=COLORS["primary"], width=2),
            fill="tozeroy",
            fillcolor="rgba(46, 117, 182, 0.1)",
        )
    )

    if cfg["value_format"] == "pct_change":
        fig.add_hline(
            y=0,
            line_dash="dash",
            line_color=COLORS["neutral"],
            annotation_text="Jan 2020 Baseline",
        )

    fig.update_layout(
        title=f"National {metric_label}",
        xaxis_title="Date",
        yaxis_title=metric_label,
        margin={"r": 20, "t": 40, "l": 20, "b": 20},
        height=400,
        hovermode="x unified",
    )

    return fig
