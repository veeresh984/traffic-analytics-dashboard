import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Vehicle Analysis",
    page_icon="🚗",
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
# HEADER
# =====================================================

st.title("🚗 Vehicle Analysis Dashboard")

st.markdown("""
Analyze vehicle composition, traffic contribution,
hourly patterns and vehicle behavior.
""")

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Filters")

selected_days = st.sidebar.multiselect(
    "Select Day",
    sorted(df["Day of the week"].unique()),
    default=sorted(df["Day of the week"].unique())
)

filtered_df = df[
    df["Day of the week"].isin(selected_days)
]

# =====================================================
# VEHICLE TOTALS
# =====================================================

cars = filtered_df["CarCount"].sum()
bikes = filtered_df["BikeCount"].sum()
buses = filtered_df["BusCount"].sum()
trucks = filtered_df["TruckCount"].sum()

# =====================================================
# KPI CARDS
# =====================================================

st.subheader("📊 Vehicle KPIs")

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric("Cars", f"{cars:,}")

with col2:
    st.metric("Bikes", f"{bikes:,}")

with col3:
    st.metric("Buses", f"{buses:,}")

with col4:
    st.metric("Trucks", f"{trucks:,}")

st.divider()

# =====================================================
# VEHICLE DISTRIBUTION
# =====================================================

vehicle_df = pd.DataFrame({
    "Vehicle": ["Cars","Bikes","Buses","Trucks"],
    "Count": [cars,bikes,buses,trucks]
})

col1,col2 = st.columns(2)

with col1:

    st.subheader("🚘 Vehicle Composition")

    fig = px.pie(
        vehicle_df,
        names="Vehicle",
        values="Count",
        hole=0.6
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.subheader("📊 Vehicle Volumes")

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
# CONTRIBUTION %
# =====================================================

st.subheader("📈 Vehicle Contribution (%)")

vehicle_df["Contribution %"] = (
    vehicle_df["Count"]
    / vehicle_df["Count"].sum()
    * 100
)

fig = px.bar(
    vehicle_df,
    x="Vehicle",
    y="Contribution %",
    color="Vehicle",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# HOURLY VEHICLE TREND
# =====================================================

st.subheader("⏰ Hourly Vehicle Trends")

hourly = (
    filtered_df
    .groupby("Hour")
    [
        [
            "CarCount",
            "BikeCount",
            "BusCount",
            "TruckCount"
        ]
    ]
    .mean()
    .reset_index()
)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=hourly["Hour"],
        y=hourly["CarCount"],
        mode="lines",
        name="Cars"
    )
)

fig.add_trace(
    go.Scatter(
        x=hourly["Hour"],
        y=hourly["BikeCount"],
        mode="lines",
        name="Bikes"
    )
)

fig.add_trace(
    go.Scatter(
        x=hourly["Hour"],
        y=hourly["BusCount"],
        mode="lines",
        name="Buses"
    )
)

fig.add_trace(
    go.Scatter(
        x=hourly["Hour"],
        y=hourly["TruckCount"],
        mode="lines",
        name="Trucks"
    )
)

fig.update_layout(
    title="Hourly Vehicle Movement"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# DAYWISE VEHICLE ANALYSIS
# =====================================================

st.subheader("📅 Vehicle Traffic by Day")

day_vehicle = (
    filtered_df
    .groupby("Day of the week")
    [
        [
            "CarCount",
            "BikeCount",
            "BusCount",
            "TruckCount"
        ]
    ]
    .mean()
    .reset_index()
)

fig = px.bar(
    day_vehicle,
    x="Day of the week",
    y=[
        "CarCount",
        "BikeCount",
        "BusCount",
        "TruckCount"
    ],
    barmode="group"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# PEAK HOURS BY VEHICLE
# =====================================================

st.subheader("🔥 Peak Hour by Vehicle Type")

peak_summary = pd.DataFrame({

    "Vehicle":[
        "Cars",
        "Bikes",
        "Buses",
        "Trucks"
    ],

    "Peak Hour":[

        filtered_df.groupby("Hour")
        ["CarCount"]
        .mean()
        .idxmax(),

        filtered_df.groupby("Hour")
        ["BikeCount"]
        .mean()
        .idxmax(),

        filtered_df.groupby("Hour")
        ["BusCount"]
        .mean()
        .idxmax(),

        filtered_df.groupby("Hour")
        ["TruckCount"]
        .mean()
        .idxmax()
    ]
})

st.dataframe(
    peak_summary,
    use_container_width=True
)

# =====================================================
# VEHICLE HEATMAP
# =====================================================

st.subheader("🔥 Vehicle Heatmap (Cars)")

heatmap = (
    filtered_df
    .groupby(
        [
            "Day of the week",
            "Hour"
        ]
    )["CarCount"]
    .mean()
    .reset_index()
)

pivot = heatmap.pivot(
    index="Day of the week",
    columns="Hour",
    values="CarCount"
)

fig = px.imshow(
    pivot,
    text_auto=True,
    aspect="auto"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# CORRELATION MATRIX
# =====================================================

st.subheader("🔍 Vehicle Correlation Matrix")

corr = filtered_df[
    [
        "CarCount",
        "BikeCount",
        "BusCount",
        "TruckCount",
        "Total"
    ]
].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# INSIGHTS
# =====================================================

st.subheader("🧠 Vehicle Insights")

dominant_vehicle = vehicle_df.loc[
    vehicle_df["Count"].idxmax(),
    "Vehicle"
]

least_vehicle = vehicle_df.loc[
    vehicle_df["Count"].idxmin(),
    "Vehicle"
]

st.success(f"""
### Key Findings

✅ Dominant Vehicle Type: **{dominant_vehicle}**

✅ Least Observed Vehicle: **{least_vehicle}**

✅ Cars contribute the largest share of traffic congestion.

✅ Hourly analysis identifies peak movement periods.

✅ Correlation analysis reveals how vehicle categories
affect total traffic volume.
""")

# =====================================================
# RAW DATA
# =====================================================

with st.expander("View Vehicle Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Vehicle Analytics Dashboard | Streamlit + Plotly"
)
