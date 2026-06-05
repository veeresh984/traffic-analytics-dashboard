import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from statsmodels.tsa.holtwinters import ExponentialSmoothing

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Traffic Analytics Dashboard",
    page_icon="🚦",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.metric-card {
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 3px 10px rgba(0,0,0,0.1);
}

h1,h2,h3 {
    color:#1f4e79;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("TrafficTwoMonth.csv")

    df["Date"] = pd.to_datetime(df["Date"])

    df["Hour"] = pd.to_datetime(
        df["Time"],
        format="%H:%M:%S"
    ).dt.hour

    return df

df = load_data()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🚦 Deep Traffic Analytics Dashboard")

st.markdown(
"""
Monitor traffic flow, congestion patterns,
vehicle composition and future traffic trends.
"""
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("Filters")

days = st.sidebar.multiselect(
    "Select Day",
    options=sorted(df["Day of the week"].unique()),
    default=sorted(df["Day of the week"].unique())
)

traffic_levels = st.sidebar.multiselect(
    "Traffic Situation",
    options=df["Traffic Situation"].unique(),
    default=df["Traffic Situation"].unique()
)

filtered_df = df[
    (df["Day of the week"].isin(days))
    &
    (df["Traffic Situation"].isin(traffic_levels))
]

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

st.subheader("📊 Executive KPI Dashboard")

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "Total Vehicles",
        f"{filtered_df['Total'].sum():,.0f}"
    )

with col2:
    st.metric(
        "Average Traffic",
        f"{filtered_df['Total'].mean():.2f}"
    )

with col3:
    st.metric(
        "Peak Traffic",
        f"{filtered_df['Total'].max():,.0f}"
    )

with col4:
    st.metric(
        "Observations",
        f"{len(filtered_df):,}"
    )

st.divider()

# --------------------------------------------------
# TRAFFIC TREND
# --------------------------------------------------

st.subheader("📈 Hourly Traffic Trend")

hourly = (
    filtered_df.groupby("Hour")["Total"]
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

# --------------------------------------------------
# VEHICLE DISTRIBUTION
# --------------------------------------------------

col1,col2 = st.columns(2)

with col1:

    st.subheader("🚗 Vehicle Composition")

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

    fig = px.pie(
        vehicle_df,
        names="Vehicle",
        values="Count",
        hole=0.5
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.subheader("🚙 Vehicle Volume")

    fig = px.bar(
        vehicle_df,
        x="Vehicle",
        y="Count",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# TRAFFIC SITUATION ANALYSIS
# --------------------------------------------------

st.subheader("🚥 Traffic Situation Distribution")

traffic_dist = (
    filtered_df["Traffic Situation"]
    .value_counts()
    .reset_index()
)

traffic_dist.columns = [
    "Traffic Situation",
    "Count"
]

fig = px.bar(
    traffic_dist,
    x="Traffic Situation",
    y="Count",
    color="Traffic Situation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# DAY-WISE ANALYSIS
# --------------------------------------------------

st.subheader("📅 Day Wise Traffic")

daywise = (
    filtered_df.groupby(
        "Day of the week"
    )["Total"]
    .mean()
    .reset_index()
)

fig = px.bar(
    daywise,
    x="Day of the week",
    y="Total",
    color="Total"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# HEATMAP
# --------------------------------------------------

st.subheader("🔥 Congestion Heatmap")

heatmap_df = (
    filtered_df.groupby(
        [
            "Day of the week",
            "Hour"
        ]
    )["Total"]
    .mean()
    .reset_index()
)

pivot = heatmap_df.pivot(
    index="Day of the week",
    columns="Hour",
    values="Total"
)

fig = px.imshow(
    pivot,
    text_auto=True,
    aspect="auto",
    title="Traffic Congestion Heatmap"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# CORRELATION MATRIX
# --------------------------------------------------

st.subheader("🔍 Correlation Matrix")

corr_cols = [
    "CarCount",
    "BikeCount",
    "BusCount",
    "TruckCount",
    "Total"
]

corr = filtered_df[corr_cols].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# PEAK HOUR ANALYSIS
# --------------------------------------------------

st.subheader("⏰ Peak Hour Detection")

peak_hour = (
    filtered_df.groupby("Hour")
    ["Total"]
    .mean()
    .idxmax()
)

peak_value = (
    filtered_df.groupby("Hour")
    ["Total"]
    .mean()
    .max()
)

st.success(
    f"Peak Traffic Hour : {peak_hour}:00 | Average Volume : {peak_value:.2f}"
)

# --------------------------------------------------
# FORECASTING
# --------------------------------------------------

st.subheader("📊 Traffic Forecast")

forecast_data = (
    filtered_df.groupby("Hour")
    ["Total"]
    .mean()
)

try:

    model = ExponentialSmoothing(
        forecast_data,
        trend="add"
    )

    fit = model.fit()

    forecast = fit.forecast(12)

    forecast_df = pd.DataFrame({
        "Hour":range(
            len(forecast_data),
            len(forecast_data)+12
        ),
        "Forecast":forecast.values
    })

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y=forecast_data.values,
            mode='lines+markers',
            name='Historical'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_df["Hour"],
            y=forecast_df["Forecast"],
            mode='lines+markers',
            name='Forecast'
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

except:
    st.warning(
        "Forecast could not be generated."
    )

# --------------------------------------------------
# AI BUSINESS INSIGHTS
# --------------------------------------------------

st.subheader("🧠 Automated Insights")

busy_day = (
    filtered_df.groupby(
        "Day of the week"
    )["Total"]
    .mean()
    .idxmax()
)

least_day = (
    filtered_df.groupby(
        "Day of the week"
    )["Total"]
    .mean()
    .idxmin()
)

dominant_vehicle = vehicle_df.loc[
    vehicle_df["Count"].idxmax(),
    "Vehicle"
]

st.info(f"""
### Key Findings

✅ Peak Traffic Hour: **{peak_hour}:00**

✅ Busiest Day: **{busy_day}**

✅ Least Busy Day: **{least_day}**

✅ Dominant Vehicle Type: **{dominant_vehicle}**

✅ Average Traffic Volume: **{filtered_df['Total'].mean():.2f}**

✅ Maximum Traffic Recorded: **{filtered_df['Total'].max()}**
""")

# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

st.subheader("⬇ Download Filtered Data")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="traffic_analysis.csv",
    mime="text/csv"
)

# --------------------------------------------------
# RAW DATA
# --------------------------------------------------

with st.expander("View Raw Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

st.markdown("---")

st.caption(
    "Built using Streamlit | Plotly | Pandas | Forecasting Analytics"
)
