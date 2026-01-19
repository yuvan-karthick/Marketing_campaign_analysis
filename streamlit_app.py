import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# ---------------------------------
# Page Config
# ---------------------------------
st.set_page_config(
    page_title="Marketing Analytics Dashboard",
    layout="wide",
    page_icon="📊"
)

# ---------------------------------
# Global Styling (Bigger Fonts + Cleaner UI)
# ---------------------------------
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-size: 18px;
    }
    h1 { font-size: 40px !important; }
    h2 { font-size: 32px !important; }
    h3 { font-size: 26px !important; }
    .stMetric { font-size: 22px; }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------
# Database Connection
# ---------------------------------
@st.cache_data
def load_data():
    conn = sqlite3.connect("C:/Users/yuvan/OneDrive/Desktop/ML_projects/Marketing_campaign_analysis/data/marketing_analytics.db")
    df = pd.read_sql("SELECT * FROM customers", conn)
    conn.close()
    return df

df = load_data()

# ---------------------------------
# Sidebar Filters (Select All + Individual)
# ---------------------------------
st.sidebar.title("🎯 Filters")

# ---- Country Filter
all_countries = df["Country"].unique().tolist()

select_all_country = st.sidebar.checkbox("Select All Countries", value=True)

if select_all_country:
    country_filter = st.sidebar.multiselect(
        "Select Country",
        options=all_countries,
        default=all_countries
    )
else:
    country_filter = st.sidebar.multiselect(
        "Select Country",
        options=all_countries
    )

# ---- Segment Filter
all_segments = df["Customer_Segment"].unique().tolist()

select_all_segment = st.sidebar.checkbox("Select All Segments", value=True)

if select_all_segment:
    segment_filter = st.sidebar.multiselect(
        "Select Customer Segment",
        options=all_segments,
        default=all_segments
    )
else:
    segment_filter = st.sidebar.multiselect(
        "Select Customer Segment",
        options=all_segments
    )

# Apply filters

df_filtered = df[
    (df["Country"].isin(country_filter)) &
    (df["Customer_Segment"].isin(segment_filter))
]

# ---------------------------------
# Title
# ---------------------------------
st.title("📊 Retail Marketing Analytics Dashboard")
st.caption("Interactive dashboard for campaign & customer insights")

# ---------------------------------
# SECTION 1 — OVERVIEW KPIs
# ---------------------------------
st.subheader("🔹 Overview KPIs")

col1, col2, col3, col4 = st.columns(4)

total_customers = df_filtered.shape[0]
overall_response = round(df_filtered["Response"].mean() * 100, 2)
avg_spend = round(df_filtered["Total_Spend"].mean(), 2)
high_spender_pct = round(
    (df_filtered["Customer_Segment"] == "High Spender").mean() * 100, 2
)

col1.metric("👥 Total Customers", total_customers)
col2.metric("📈 Response Rate (%)", overall_response)
col3.metric("💰 Avg Spend", avg_spend)
col4.metric("🔥 High Spenders (%)", high_spender_pct)

# ---------------------------------
# SECTION 2 — SEGMENT PERFORMANCE
# ---------------------------------
st.subheader("🔹 Segment Performance")

segment_perf = (
    df_filtered.groupby("Customer_Segment")
    .agg(
        customers=("ID", "count"),
        avg_spend=("Total_Spend", "mean"),
        response_rate=("Response", "mean")
    )
    .reset_index()
)

segment_perf["response_rate"] = segment_perf["response_rate"] * 100

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        segment_perf,
        x="Customer_Segment",
        y="response_rate",
        color="Customer_Segment",
        title="Response Rate by Segment",
        labels={"response_rate": "Response Rate (%)"}
    )
    fig.update_layout(font=dict(size=18), title_font_size=24)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        segment_perf,
        x="Customer_Segment",
        y="avg_spend",
        color="Customer_Segment",
        title="Average Spend by Segment",
        labels={"avg_spend": "Average Spend"}
    )
    fig.update_layout(font=dict(size=18), title_font_size=24)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# SECTION 3 — CAMPAIGN PERFORMANCE
# ---------------------------------
st.subheader("🔹 Campaign Performance")

campaign_perf = pd.DataFrame({
    "Campaign": ["Cmp1", "Cmp2", "Cmp3", "Cmp4", "Cmp5"],
    "Response Rate (%)": [
        df_filtered["AcceptedCmp1"].mean() * 100,
        df_filtered["AcceptedCmp2"].mean() * 100,
        df_filtered["AcceptedCmp3"].mean() * 100,
        df_filtered["AcceptedCmp4"].mean() * 100,
        df_filtered["AcceptedCmp5"].mean() * 100
    ]
})

fig = px.bar(
    campaign_perf,
    x="Campaign",
    y="Response Rate (%)",
    color="Campaign",
    title="Campaign Response Comparison"
)

fig.update_layout(font=dict(size=18), title_font_size=24)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# SECTION 4 — CHANNEL BEHAVIOR
# ---------------------------------
st.subheader("🔹 Channel Usage by Segment")

channel_usage = (
    df_filtered.groupby("Customer_Segment")
    .agg(
        Web=("NumWebPurchases", "mean"),
        Catalog=("NumCatalogPurchases", "mean"),
        Store=("NumStorePurchases", "mean")
    )
    .reset_index()
)

fig = px.bar(
    channel_usage,
    x="Customer_Segment",
    y=["Web", "Catalog", "Store"],
    title="Average Channel Purchases by Segment",
    barmode="group"
)

fig.update_layout(font=dict(size=18), title_font_size=24)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# SECTION 5 — UNDER-SERVED SEGMENTS 🔥
# ---------------------------------
st.subheader("🔹 Under-Served High Engagement Segments")

underserved = (
    df_filtered.groupby("Customer_Segment")
    .agg(
        customers=("ID", "count"),
        avg_web_visits=("NumWebVisitsMonth", "mean"),
        response_rate=("Response", "mean"),
        avg_spend=("Total_Spend", "mean")
    )
    .reset_index()
)

underserved["response_rate"] = underserved["response_rate"] * 100

underserved = underserved[
    (underserved["avg_web_visits"] > 5) &
    (underserved["response_rate"] < 10)
].sort_values("avg_web_visits", ascending=False)

st.dataframe(underserved, use_container_width=True)
