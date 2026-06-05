import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Traffic Patterns",
    page_icon="📈",
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

    df["Month"] = df["Date"].dt.month

    return df

df = load_data()

# =====================================================
# HEADER
# =====================================================

st.title("📈 Traffic Pattern Analysis")

st.markdown("""
Analyze traffic flow patterns across hours, days,
and congestion levels to identify peak traffic periods.
""")

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Filters")

selected_days = st.sidebar.multiselect(
    "Day of Week",
    options=sorted(df["Day of the week"].unique()),
    default=sorted(df["Day of the week"].unique())
)

filtered_df = df[
    df["Day of the week"].isin(selected_days)
]

# =====================================================
# KPI SECTION
# =====================================================

avg_traffic = filtered_df["Total"].mean()

peak_hour = (
    filtered_df.groupby("Hour")["Total"]
    .mean()
    .idxmax()
)

peak_traffic = (
    filtered_df.groupby("Hour")["Total"]
    .mean()
    .max()
)

peak_day = (
    filtered_df.groupby("Day of the week")["Total"]
    .mean()
    .idxmax()
)

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "Average Traffic",
        f"{avg_traffic:.2f}"
    )

with col2:
    st.metric(
        "Peak Hour",
        f"{peak_hour}:00"
    )

with col3:
    st.metric(
        "Peak Volume",
        f"{peak_traffic:.0f}"
    )

with col4:
    st.metric(
        "Busiest Day",
        peak_day
    )

st.divider()

# =====================================================
# HOURLY TRAFFIC TREND
# =====================================================

st.subheader("⏰ Hourly Traffic Trend")

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

# =====================================================
# DAILY TRAFFIC TREND
# =====================================================

st.subheader("📅 Daily Traffic Trend")

daily = (
    filtered_df
    .groupby("Day of the week")["Total"]
    .mean()
    .reset_index()
)

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

daily["Day of the week"] = pd.Categorical(
    daily["Day of the week"],
    categories=day_order,
    ordered=True
)

daily = daily.sort_values(
    "Day of the week"
)

fig = px.bar(
    daily,
    x="Day of the week",
    y="Total",
    color="Total",
    text_auto=".2f",
    title="Average Traffic by Day"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# WEEKDAY VS WEEKEND
# =====================================================

st.subheader("📊 Weekday vs Weekend Analysis")

filtered_df["Category"] = filtered_df[
    "Day of the week"
].apply(
    lambda x:
    "Weekend"
    if x in ["Saturday","Sunday"]
    else "Weekday"
)

week_comp = (
    filtered_df
    .groupby("Category")["Total"]
    .mean()
    .reset_index()
)

fig = px.pie(
    week_comp,
    names="Category",
    values="Total",
    hole=0.5
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# TRAFFIC SITUATION BY HOUR
# =====================================================

st.subheader("🚦 Traffic Situation Across Hours")

traffic_hour = (
    filtered_df
    .groupby(
        ["Hour","Traffic Situation"]
    )["Total"]
    .mean()
    .reset_index()
)

fig = px.area(
    traffic_hour,
    x="Hour",
    y="Total",
    color="Traffic Situation",
    title="Traffic Situation by Hour"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# HEATMAP
# =====================================================

st.subheader("🔥 Traffic Congestion Heatmap")

heatmap = (
    filtered_df
    .groupby(
        ["Day of the week","Hour"]
    )["Total"]
    .mean()
    .reset_index()
)

pivot = heatmap.pivot(
    index="Day of the week",
    columns="Hour",
    values="Total"
)

fig = px.imshow(
    pivot,
    text_auto=True,
    aspect="auto",
    title="Traffic Density Heatmap"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# TOP 10 BUSIEST HOURS
# =====================================================

st.subheader("🏆 Top 10 Busiest Hours")

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
# TRAFFIC DISTRIBUTION
# =====================================================

st.subheader("📉 Traffic Distribution")

fig = px.histogram(
    filtered_df,
    x="Total",
    nbins=40,
    marginal="box",
    title="Traffic Volume Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# MOVING AVERAGE TREND
# =====================================================

st.subheader("📊 Moving Average Trend")

trend = (
    filtered_df
    .groupby("Date")["Total"]
    .mean()
    .reset_index()
)

trend["7_Day_MA"] = (
    trend["Total"]
    .rolling(7)
    .mean()
)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=trend["Date"],
        y=trend["Total"],
        mode="lines",
        name="Daily Average"
    )
)

fig.add_trace(
    go.Scatter(
        x=trend["Date"],
        y=trend["7_Day_MA"],
        mode="lines",
        name="7-Day Moving Average"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# BUSINESS INSIGHTS
# =====================================================

st.subheader("🧠 Pattern Insights")

lowest_day = (
    filtered_df
    .groupby("Day of the week")["Total"]
    .mean()
    .idxmin()
)

st.success(f"""
### Key Traffic Insights

✅ Peak Hour: **{peak_hour}:00**

✅ Peak Traffic Volume: **{peak_traffic:.0f}**

✅ Busiest Day: **{peak_day}**

✅ Least Busy Day: **{lowest_day}**

✅ Average Traffic Volume: **{avg_traffic:.2f}**

✅ Traffic surges occur during identified rush hours.

✅ Heatmap reveals congestion concentration across the week.
""")

# =====================================================
# RAW DATA
# =====================================================

with st.expander("View Processed Data"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Traffic Pattern Analytics | Streamlit + Plotly"
)
