import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from statsmodels.tsa.holtwinters import ExponentialSmoothing

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Traffic Forecasting",
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

    return df

df = load_data()

# =====================================================
# HEADER
# =====================================================

st.title("📈 Traffic Forecasting Dashboard")

st.markdown("""
Forecast future traffic demand using historical traffic data.

The model uses Holt-Winters Exponential Smoothing
to estimate future traffic volumes.
""")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Forecast Settings")

forecast_days = st.sidebar.slider(
    "Forecast Horizon (Days)",
    min_value=7,
    max_value=30,
    value=14
)

# =====================================================
# DAILY AGGREGATION
# =====================================================

daily_traffic = (
    df.groupby("Date")["Total"]
    .mean()
    .reset_index()
)

daily_traffic = daily_traffic.sort_values("Date")

# =====================================================
# KPI SECTION
# =====================================================

avg_daily = daily_traffic["Total"].mean()

max_daily = daily_traffic["Total"].max()

min_daily = daily_traffic["Total"].min()

growth = (
    (
        daily_traffic["Total"].iloc[-1]
        -
        daily_traffic["Total"].iloc[0]
    )
    /
    daily_traffic["Total"].iloc[0]
) * 100

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "Average Daily Traffic",
        f"{avg_daily:.2f}"
    )

with col2:
    st.metric(
        "Highest Daily Traffic",
        f"{max_daily:.0f}"
    )

with col3:
    st.metric(
        "Lowest Daily Traffic",
        f"{min_daily:.0f}"
    )

with col4:
    st.metric(
        "Growth %",
        f"{growth:.2f}%"
    )

st.divider()

# =====================================================
# HISTORICAL TREND
# =====================================================

st.subheader("📊 Historical Traffic Trend")

fig = px.line(
    daily_traffic,
    x="Date",
    y="Total",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# MOVING AVERAGE
# =====================================================

st.subheader("📈 Moving Average Trend")

daily_traffic["7 Day MA"] = (
    daily_traffic["Total"]
    .rolling(7)
    .mean()
)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=daily_traffic["Date"],
        y=daily_traffic["Total"],
        mode="lines",
        name="Actual Traffic"
    )
)

fig.add_trace(
    go.Scatter(
        x=daily_traffic["Date"],
        y=daily_traffic["7 Day MA"],
        mode="lines",
        name="7 Day Moving Average"
    )
)

fig.update_layout(
    title="Traffic Trend with Moving Average"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# FORECAST MODEL
# =====================================================

st.subheader("🔮 Traffic Forecast")

series = daily_traffic["Total"]

try:

    model = ExponentialSmoothing(
        series,
        trend="add",
        seasonal=None
    )

    fit = model.fit()

    forecast = fit.forecast(forecast_days)

    future_dates = pd.date_range(
        start=daily_traffic["Date"].max()
        + pd.Timedelta(days=1),
        periods=forecast_days
    )

    forecast_df = pd.DataFrame({
        "Date": future_dates,
        "Forecast": forecast.values
    })

    # Confidence Band (Approximation)

    std_dev = series.std()

    forecast_df["Upper"] = (
        forecast_df["Forecast"]
        + (1.96 * std_dev)
    )

    forecast_df["Lower"] = (
        forecast_df["Forecast"]
        - (1.96 * std_dev)
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=daily_traffic["Date"],
            y=daily_traffic["Total"],
            mode="lines",
            name="Historical"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_df["Date"],
            y=forecast_df["Forecast"],
            mode="lines+markers",
            name="Forecast"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_df["Date"],
            y=forecast_df["Upper"],
            mode="lines",
            line=dict(width=0),
            showlegend=False
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_df["Date"],
            y=forecast_df["Lower"],
            mode="lines",
            fill="tonexty",
            line=dict(width=0),
            name="Confidence Range"
        )
    )

    fig.update_layout(
        title="Traffic Forecast"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

except Exception as e:

    st.error(
        f"Forecasting Error: {e}"
    )

# =====================================================
# FORECAST TABLE
# =====================================================

st.subheader("📋 Forecast Output")

st.dataframe(
    forecast_df,
    use_container_width=True
)

# =====================================================
# FORECAST DISTRIBUTION
# =====================================================

st.subheader("📉 Forecast Distribution")

fig = px.histogram(
    forecast_df,
    x="Forecast",
    nbins=20,
    marginal="box"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# FORECAST SUMMARY
# =====================================================

st.subheader("📌 Forecast Summary")

future_avg = forecast_df["Forecast"].mean()

future_peak = forecast_df["Forecast"].max()

future_min = forecast_df["Forecast"].min()

col1,col2,col3 = st.columns(3)

with col1:
    st.metric(
        "Future Average",
        f"{future_avg:.2f}"
    )

with col2:
    st.metric(
        "Future Peak",
        f"{future_peak:.2f}"
    )

with col3:
    st.metric(
        "Future Minimum",
        f"{future_min:.2f}"
    )

# =====================================================
# INSIGHTS
# =====================================================

st.subheader("🧠 Forecast Insights")

trend_direction = (
    "Increasing"
    if forecast_df["Forecast"].iloc[-1]
    >
    forecast_df["Forecast"].iloc[0]
    else "Decreasing"
)

st.success(f"""
### Forecast Highlights

✅ Forecast Horizon: **{forecast_days} Days**

✅ Expected Average Traffic:
**{future_avg:.2f}**

✅ Highest Predicted Traffic:
**{future_peak:.2f}**

✅ Lowest Predicted Traffic:
**{future_min:.2f}**

✅ Traffic Trend:
**{trend_direction}**

✅ Forecast generated using
Holt-Winters Exponential Smoothing.
""")

# =====================================================
# DOWNLOAD FORECAST
# =====================================================

st.subheader("⬇ Download Forecast")

csv = forecast_df.to_csv(index=False)

st.download_button(
    label="Download Forecast CSV",
    data=csv,
    file_name="traffic_forecast.csv",
    mime="text/csv"
)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Traffic Forecasting Dashboard | Streamlit + Statsmodels"
)
