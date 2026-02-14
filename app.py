"""Economic Tracker Dashboard - Landing Page."""

import streamlit as st

from src.config import DATASETS, NATIONAL_URLS
from src.data_loader import get_national_data
from src.charts import build_national_chart

st.set_page_config(
    page_title="Economic Tracker",
    page_icon="\U0001f4c8",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for metric cards
st.markdown(
    """
<style>
    .metric-card {
        background: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2e75b6;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #666;
        margin-top: 4px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Hero section
st.title("\U0001f4c8 Economic Tracker Dashboard")
st.markdown(
    "Track COVID-era economic recovery across U.S. counties using "
    "[Opportunity Insights](https://opportunityinsights.org/) data. "
    "Explore employment, consumer spending, job postings, unemployment claims, "
    "and student progress \u2014 updated regularly from public data sources."
)

st.divider()

# Summary metric cards
st.subheader("National Snapshot")
summary_items = [
    ("employment", "emp", "Employment"),
    ("spending", "spend_all", "Spending"),
    ("unemployment", "initclaims_rate_regular", "UI Claims Rate"),
    ("job_postings", "bg_posts", "Job Postings"),
]

cols = st.columns(len(summary_items))
for i, (key, metric, label) in enumerate(summary_items):
    with cols[i]:
        try:
            data = get_national_data(key)
            if data is not None and metric in data.columns:
                latest = data.dropna(subset=[metric])[metric].iloc[-1]
                cfg = DATASETS[key]
                if cfg["value_format"] == "pct_change":
                    display = f"{latest * 100:+.1f}%"
                else:
                    display = f"{latest:.2f}"
                st.metric(label=f"{cfg['icon']} {label}", value=display)
            else:
                st.metric(label=label, value="N/A")
        except Exception:
            st.metric(label=label, value="N/A")

st.divider()

# National overview chart
st.subheader("National Trends")

available_datasets = [k for k in DATASETS if k in NATIONAL_URLS]
chart_dataset = st.selectbox(
    "Select dataset",
    options=available_datasets,
    format_func=lambda x: f"{DATASETS[x]['icon']} {DATASETS[x]['title']}",
)

if chart_dataset:
    cfg = DATASETS[chart_dataset]
    chart_metric = st.selectbox(
        "Select metric",
        options=list(cfg["metrics"].keys()),
        format_func=lambda x: cfg["metrics"][x],
        key="landing_metric",
    )

    data = get_national_data(chart_dataset)
    if data is not None:
        fig = build_national_chart(data, chart_dataset, chart_metric)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

st.divider()

# Data source attribution
st.subheader("About the Data")
st.markdown(
    "Data sourced from the "
    "[Opportunity Insights Economic Tracker]"
    "(https://github.com/OpportunityInsights/EconomicTracker), "
    "a publicly available dataset tracking economic activity across the "
    "United States during and after COVID-19."
)
st.markdown("**Datasets included:**")
for cfg in DATASETS.values():
    st.markdown(f"- {cfg['icon']} **{cfg['title']}** \u2014 Source: {cfg['source']}")

st.caption(
    "Data is cached for 24 hours. Navigate to individual pages using the sidebar "
    "to explore county-level maps and time-series charts."
)
