import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    df = pd.read_csv("data/TrafficTwoMonth.csv")

    df.columns = df.columns.str.strip()

    df["Date"] = pd.to_datetime(df["Date"])

    df["Time"] = pd.to_datetime(df["Time"])

    df["Hour"] = df["Time"].dt.hour

    return df

df = load_data()

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Dashboard Filters")

selected_days = st.sidebar.multiselect(
    "Day of Week",
    options=sorted(df["Day of the week"].unique()),
    default=sorted(df["Day of the week"].unique())
)

selected_traffic = st.sidebar.multiselect(
    "Traffic Situation",
    options=sorted(df["Traffic Situation"].unique()),
    default=sorted(df["Traffic Situation"].unique())
)

filtered_df = df[
    (df["Day of the week"].isin(selected_days))
    &
    (df["Traffic Situation"].isin(selected_traffic))
]

# =====================================================
# HEADER
# =====================================================

st.title("📊 Executive Traffic Dashboard")

st.markdown(
"""
Executive overview of traffic volume, congestion,
vehicle distribution and operational insights.
"""
)

# =====================================================
# KPI CARDS
# =====================================================

total_traffic = filtered_df["Total"].sum()

avg_traffic = filtered_df["Total"].mean()

max_traffic = filtered_df["Total"].max()

records = len(filtered_df)

peak_hour = (
    filtered_df
    .groupby("Hour")["Total"]
    .mean()
    .idxmax()
)

col1,col2,col3,col4,col5 = st.columns(5)

with col1:
    st.metric(
        "Total Vehicles",
        f"{total_traffic:,.0f}"
    )

with col2:
    st.metric(
        "Average Traffic",
        f"{avg_traffic:.2f}"
    )

with col3:
    st.metric(
        "Peak Traffic",
        f"{max_traffic:,.0f}"
    )

with col4:
    st.metric(
        "Records",
        f"{records:,}"
    )

with col5:
    st.metric(
        "Peak Hour",
        f"{peak_hour}:00"
    )

st.divider()

# =====================================================
# TRAFFIC TREND
# =====================================================

col1,col2 = st.columns(2)

with col1:

    st.subheader("📈 Hourly Traffic Trend")

    hourly = (
        filtered_df
        .groupby("Hour")["Total"]
        .mean()
        .reset_index()
    )

    fig = px.line(
        hourly,
        x="Hour",
        y="Total",
        markers=True,
        title="Average Traffic by Hour"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.subheader("📅 Daily Traffic")

    daily = (
        filtered_df
        .groupby("Day of the week")["Total"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        daily,
        x="Day of the week",
        y="Total",
        color="Total",
        text_auto=".1f"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# VEHICLE DISTRIBUTION
# =====================================================

st.subheader("🚗 Vehicle Distribution")

vehicle_df = pd.DataFrame({

    "Vehicle":[
        "Cars",
        "Bikes",
        "Bus",
        "Truck"
    ],

    "Count":[
        filtered_df["CarCount"].sum(),
        filtered_df["BikeCount"].sum(),
        filtered_df["BusCount"].sum(),
        filtered_df["TruckCount"].sum()
    ]

})

col1,col2 = st.columns(2)

with col1:

    fig = px.pie(
        vehicle_df,
        names="Vehicle",
        values="Count",
        hole=0.55
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.bar(
        vehicle_df,
        x="Vehicle",
        y="Count",
        color="Vehicle",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# TRAFFIC SITUATION
# =====================================================

st.subheader("🚦 Traffic Situation Overview")

situation = (
    filtered_df["Traffic Situation"]
    .value_counts()
    .reset_index()
)

situation.columns = [
    "Traffic Situation",
    "Count"
]

fig = px.bar(
    situation,
    x="Traffic Situation",
    y="Count",
    color="Traffic Situation",
    text_auto=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# TOP CONGESTION HOURS
# =====================================================

st.subheader("🔥 Top Congestion Hours")

top_hours = (
    filtered_df
    .groupby("Hour")["Total"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_hours,
    x="Hour",
    y="Total",
    color="Total",
    text_auto=".1f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# EXECUTIVE INSIGHTS
# =====================================================

st.subheader("🧠 Executive Insights")

busy_day = (
    filtered_df
    .groupby("Day of the week")["Total"]
    .mean()
    .idxmax()
)

least_day = (
    filtered_df
    .groupby("Day of the week")["Total"]
    .mean()
    .idxmin()
)

dominant_vehicle = vehicle_df.loc[
    vehicle_df["Count"].idxmax(),
    "Vehicle"
]

st.success(f"""
Peak traffic is observed at **{peak_hour}:00**.

The busiest day is **{busy_day}**.

The least busy day is **{least_day}**.

The dominant vehicle category is **{dominant_vehicle}**.

Average traffic volume is **{avg_traffic:.2f} vehicles**.
""")

# =====================================================
# TRAFFIC SUMMARY TABLE
# =====================================================

st.subheader("📋 Summary Statistics")

summary = filtered_df[
    [
        "CarCount",
        "BikeCount",
        "BusCount",
        "TruckCount",
        "Total"
    ]
].describe()

st.dataframe(
    summary,
    use_container_width=True
)

# =====================================================
# DOWNLOAD DATA
# =====================================================

st.subheader("⬇ Export Data")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Dataset",
    data=csv,
    file_name="executive_dashboard_export.csv",
    mime="text/csv"
)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Executive Traffic Analytics Dashboard | Streamlit + Plotly"
)

