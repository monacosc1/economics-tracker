"""Dataset configurations, column name mappings, and URLs for the Economic Tracker."""

# Opportunity Insights Economic Tracker data URLs (county-level)
DATA_URLS = {
    "spending": (
        "https://raw.githubusercontent.com/OpportunityInsights/"
        "EconomicTracker/main/data/Affinity%20-%20County%20-%20Monthly.csv"
    ),
    "employment": (
        "https://raw.githubusercontent.com/OpportunityInsights/"
        "EconomicTracker/main/data/Employment%20-%20County%20-%20Weekly.csv"
    ),
    "job_postings": (
        "https://raw.githubusercontent.com/OpportunityInsights/"
        "EconomicTracker/main/data/Job%20Postings%20-%20County%20-%20Weekly.csv"
    ),
    "unemployment": (
        "https://raw.githubusercontent.com/OpportunityInsights/"
        "EconomicTracker/main/data/UI%20Claims%20-%20County%20-%20Weekly.csv"
    ),
    "student_progress": (
        "https://raw.githubusercontent.com/OpportunityInsights/"
        "EconomicTracker/main/data/Zearn%20-%20County%20-%20Weekly.csv"
    ),
}

# National-level URLs for landing page summaries
NATIONAL_URLS = {
    "spending": (
        "https://raw.githubusercontent.com/OpportunityInsights/"
        "EconomicTracker/main/data/Affinity%20-%20National%20-%20Monthly.csv"
    ),
    "employment": (
        "https://raw.githubusercontent.com/OpportunityInsights/"
        "EconomicTracker/main/data/Employment%20-%20National%20-%20Weekly.csv"
    ),
    "job_postings": (
        "https://raw.githubusercontent.com/OpportunityInsights/"
        "EconomicTracker/main/data/Job%20Postings%20-%20National%20-%20Weekly.csv"
    ),
    "unemployment": (
        "https://raw.githubusercontent.com/OpportunityInsights/"
        "EconomicTracker/main/data/UI%20Claims%20-%20National%20-%20Weekly.csv"
    ),
}

# Dataset configurations
DATASETS = {
    "spending": {
        "title": "Consumer Spending",
        "icon": "\U0001f4b3",
        "description": (
            "Consumer spending data from Affinity Solutions, tracking credit and "
            "debit card spending across merchant categories. Values represent "
            "percentage change relative to the January 2020 baseline."
        ),
        "date_cols": ["year", "month", "day_endofmonth"],
        "metrics": {
            "spend_all": "Total Spending (Seasonally Adjusted)",
            "spend_s_all": "Total Spending (Not Adjusted)",
        },
        "drop_cols": ["freq", "provisional"],
        "baseline": "Jan 6 \u2013 Feb 2, 2020",
        "source": "Affinity Solutions",
        "value_format": "pct_change",
    },
    "employment": {
        "title": "Employment",
        "icon": "\U0001f454",
        "description": (
            "Employment levels from Paychex and Intuit payroll data. Values "
            "represent percentage change in employment relative to the "
            "January 2020 baseline."
        ),
        "date_cols": ["year", "month", "day_endofweek"],
        "metrics": {
            "emp": "Overall Employment",
            "emp_incq1": "Bottom Quartile Wages",
            "emp_incq2": "2nd Quartile Wages",
            "emp_incq3": "3rd Quartile Wages",
            "emp_incq4": "Top Quartile Wages",
            "emp_incbelowmed": "Below Median Wages",
            "emp_incabovemed": "Above Median Wages",
        },
        "drop_cols": ["emp_incmiddle"],
        "baseline": "Jan 4\u201331, 2020",
        "source": "Paychex, Intuit",
        "value_format": "pct_change",
    },
    "job_postings": {
        "title": "Job Postings",
        "icon": "\U0001f4cb",
        "description": (
            "New job postings from Lightcast (formerly Burning Glass Technologies). "
            "Values represent percentage change relative to the January 2020 baseline."
        ),
        "date_cols": ["year", "month", "day_endofweek"],
        "metrics": {
            "bg_posts": "All Job Postings",
            "bg_posts_jzgrp12": "Low-Preparation Jobs (Zones 1\u20132)",
            "bg_posts_jzgrp345": "Mid-to-High Preparation Jobs (Zones 3\u20135)",
        },
        "drop_cols": [],
        "baseline": "Jan 4\u201331, 2020",
        "source": "Lightcast (Burning Glass)",
        "value_format": "pct_change",
    },
    "unemployment": {
        "title": "Unemployment Claims",
        "icon": "\U0001f4ca",
        "description": (
            "Initial unemployment insurance claims from the Department of Labor "
            "and state agencies. Claims rate is per 100 people in the 2019 "
            "labor force."
        ),
        "date_cols": ["year", "month", "day_endofweek"],
        "metrics": {
            "initclaims_rate_regular": "Initial Claims Rate (per 100 workers)",
            "initclaims_count_regular": "Initial Claims Count",
        },
        "drop_cols": [],
        "baseline": "N/A (raw counts and rates)",
        "source": "Department of Labor",
        "value_format": "rate",
    },
    "student_progress": {
        "title": "Student Progress",
        "icon": "\U0001f4da",
        "description": (
            "Student engagement and achievement data from Zearn, an online math "
            "learning platform. Values represent percentage change relative to "
            "the January\u2013February 2020 baseline."
        ),
        "date_cols": ["year", "month", "day_endofweek"],
        "metrics": {
            "engagement": "Student Engagement",
            "badges": "Badges Earned",
        },
        "drop_cols": ["break_engagement", "break_badges", "imputed_from_cz"],
        "baseline": "Jan 6 \u2013 Feb 21, 2020",
        "source": "Zearn",
        "value_format": "pct_change",
    },
}

# Color scheme
COLORS = {
    "primary": "#2e75b6",
    "secondary": "#e8ecf1",
    "accent": "#ff6b35",
    "positive": "#28a745",
    "negative": "#dc3545",
    "neutral": "#6c757d",
    "background": "#f8f9fa",
    "chart_colors": [
        "#2e75b6", "#ff6b35", "#28a745", "#dc3545",
        "#6f42c1", "#fd7e14", "#20c997", "#e83e8c",
    ],
}
