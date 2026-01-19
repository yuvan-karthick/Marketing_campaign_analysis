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
# Navigation (Pages)
# ---------------------------------
page = st.sidebar.radio(
    "📄 Navigate",
    [
        "Segment Performance",
        "Campaign Performance",
        "Channel Usage",
        "Insights & Conclusions"
    ]
)

# ---------------------------------
# PAGE 1 — SEGMENT PERFORMANCE
# ---------------------------------
if page == "Segment Performance":

    st.title("📊 Segment Performance")
    st.caption("True engagement & value by customer segment")

    # Create proper engagement variable
    df_filtered = df_filtered.copy()
    df_filtered["Any_Response"] = (
        df_filtered["AcceptedCmp1"] +
        df_filtered["AcceptedCmp2"] +
        df_filtered["AcceptedCmp3"] +
        df_filtered["AcceptedCmp4"] +
        df_filtered["AcceptedCmp5"]
    ) > 0

    # Exclude Campaign Responder
    df_no_campaign = df_filtered[
        ~df_filtered["Customer_Segment"].isin(["Campaign Responder", "Campaign Responders"])
    ]

    segment_perf = (
        df_no_campaign.groupby("Customer_Segment")
        .agg(
            customers=("ID", "count"),
            avg_spend=("Total_Spend", "mean"),
            response_rate=("Any_Response", "mean")
        )
        .reset_index()
    )

    segment_perf["response_rate"] *= 100
    segment_perf = segment_perf.sort_values("response_rate", ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            segment_perf,
            x="Customer_Segment",
            y="response_rate",
            color="Customer_Segment",
            title="True Campaign Engagement by Segment",
            labels={"response_rate": "Engagement Rate (%)"}
        )
        fig.update_layout(font=dict(size=18), title_font_size=26)
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
        fig.update_layout(font=dict(size=18), title_font_size=26)
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# PAGE 2 — CAMPAIGN PERFORMANCE
# ---------------------------------
elif page == "Campaign Performance":

    st.title("🎯 Campaign Performance")
    st.caption("Which campaigns performed best")

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

    fig.update_layout(font=dict(size=18), title_font_size=26)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# PAGE 3 — CHANNEL USAGE
# ---------------------------------
elif page == "Channel Usage":

    st.title("🛒 Channel Usage by Segment")
    st.caption("How different segments prefer to purchase")

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

    fig.update_layout(font=dict(size=18), title_font_size=26)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# PAGE 4 — INSIGHTS & CONCLUSIONS 🔥
# ---------------------------------
elif page == "Insights & Conclusions":

    st.title("🚀 Strategic Insights & Conclusions")
    st.caption("Key business takeaways from the analysis")

    # Recompute segment performance for insights
    df_filtered = df_filtered.copy()
    df_filtered["Any_Response"] = (
        df_filtered["AcceptedCmp1"] +
        df_filtered["AcceptedCmp2"] +
        df_filtered["AcceptedCmp3"] +
        df_filtered["AcceptedCmp4"] +
        df_filtered["AcceptedCmp5"]
    ) > 0

    df_no_campaign = df_filtered[
        ~df_filtered["Customer_Segment"].isin(["Campaign Responder", "Campaign Responders"])
    ]

    insight_table = (
        df_no_campaign.groupby("Customer_Segment")
        .agg(
            customers=("ID", "count"),
            avg_spend=("Total_Spend", "mean"),
            response_rate=("Any_Response", "mean")
        )
        .reset_index()
    )

    insight_table["response_rate"] *= 100
    insight_table = insight_table.sort_values("response_rate", ascending=False)

    # Small table (underserved)
    st.subheader("🔹 Under-Served High Engagement Segments")

    underserved = (
        df_no_campaign.groupby("Customer_Segment")
        .agg(
            customers=("ID", "count"),
            avg_web_visits=("NumWebVisitsMonth", "mean"),
            response_rate=("Any_Response", "mean"),
            avg_spend=("Total_Spend", "mean")
        )
        .reset_index()
    )

    underserved["response_rate"] *= 100

    underserved = underserved[
        (underserved["avg_web_visits"] > 5) &
        (underserved["response_rate"] < 15)
    ].sort_values("avg_web_visits", ascending=False)

    st.dataframe(underserved, use_container_width=True)

    # Fun Conclusions 🎉
    st.subheader("🌟 Key Strategic Conclusions")

    top_segment = insight_table.iloc[0]
    second_segment = insight_table.iloc[1]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### 🥇 Most Valuable Segment
        **{seg}**  
        💰 Avg Spend: {spend:.2f}  
        📈 Engagement: {rate:.2f}%  
        """.format(
            seg=top_segment["Customer_Segment"],
            spend=top_segment["avg_spend"],
            rate=top_segment["response_rate"]
        ))

    with col2:
        st.markdown("""
        ### 🥈 Secondary Growth Segment
        **{seg}**  
        💰 Avg Spend: {spend:.2f}  
        📈 Engagement: {rate:.2f}%  
        """.format(
            seg=second_segment["Customer_Segment"],
            spend=second_segment["avg_spend"],
            rate=second_segment["response_rate"]
        ))

    with col3:
        most_responsive = insight_table.sort_values("response_rate", ascending=False).iloc[0]

        st.markdown("""
        ### ⚡ Most Responsive Segment
        **{seg}**  
        📈 Engagement: {rate:.2f}%  
        👥 Customers: {cust}  
        """.format(
            seg=most_responsive["Customer_Segment"],
            rate=most_responsive["response_rate"],
            cust=int(most_responsive["customers"])
        ))

    st.success("🎯 **Business Recommendation:** Focus primary campaigns on the most valuable & responsive segments, while nurturing under-served high-engagement groups for future growth.")
