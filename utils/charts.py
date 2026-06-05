import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# =====================================================
# KPI STYLE COLORS
# =====================================================

COLOR_SEQUENCE = px.colors.qualitative.Set2

# =====================================================
# HOURLY TRAFFIC TREND
# =====================================================

def plot_hourly_trend(df):

    hourly = (
        df.groupby("Hour")["Total"]
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

    fig.update_layout(
        template="plotly_white",
        hovermode="x unified"
    )

    return fig


# =====================================================
# DAILY TRAFFIC TREND
# =====================================================

def plot_daily_trend(df):

    daily = (
        df.groupby("Day of the week")["Total"]
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

    fig.update_layout(
        template="plotly_white"
    )

    return fig


# =====================================================
# VEHICLE PIE CHART
# =====================================================

def plot_vehicle_distribution(vehicle_df):

    fig = px.pie(
        vehicle_df,
        names="Vehicle",
        values="Count",
        hole=0.55,
        title="Vehicle Distribution"
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig


# =====================================================
# VEHICLE BAR CHART
# =====================================================

def plot_vehicle_bar(vehicle_df):

    fig = px.bar(
        vehicle_df,
        x="Vehicle",
        y="Count",
        color="Vehicle",
        text_auto=True,
        title="Vehicle Counts"
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig


# =====================================================
# VEHICLE CONTRIBUTION
# =====================================================

def plot_vehicle_contribution(vehicle_df):

    fig = px.bar(
        vehicle_df,
        x="Vehicle",
        y="Contribution %",
        color="Vehicle",
        text_auto=".2f",
        title="Vehicle Contribution (%)"
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig


# =====================================================
# TRAFFIC SITUATION
# =====================================================

def plot_traffic_situation(df):

    traffic = (
        df["Traffic Situation"]
        .value_counts()
        .reset_index()
    )

    traffic.columns = [
        "Traffic Situation",
        "Count"
    ]

    fig = px.bar(
        traffic,
        x="Traffic Situation",
        y="Count",
        color="Traffic Situation",
        text_auto=True,
        title="Traffic Situation Distribution"
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig


# =====================================================
# HEATMAP
# =====================================================

def plot_heatmap(df):

    heatmap = (
        df.groupby(
            [
                "Day of the week",
                "Hour"
            ]
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
        title="Traffic Heatmap"
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig


# =====================================================
# CORRELATION MATRIX
# =====================================================

def plot_correlation_matrix(df):

    corr = df[
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
        aspect="auto",
        title="Correlation Matrix"
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig


# =====================================================
# VEHICLE HOURLY TREND
# =====================================================

def plot_vehicle_hourly_trend(df):

    hourly = (
        df.groupby("Hour")[
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
        title="Vehicle Movement by Hour",
        template="plotly_white"
    )

    return fig


# =====================================================
# MOVING AVERAGE TREND
# =====================================================

def plot_moving_average(df):

    daily = (
        df.groupby("Date")["Total"]
        .mean()
        .reset_index()
    )

    daily["7_Day_MA"] = (
        daily["Total"]
        .rolling(7)
        .mean()
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=daily["Date"],
            y=daily["Total"],
            mode="lines",
            name="Traffic"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=daily["Date"],
            y=daily["7_Day_MA"],
            mode="lines",
            name="7-Day MA"
        )
    )

    fig.update_layout(
        title="Moving Average Trend",
        template="plotly_white"
    )

    return fig


# =====================================================
# FORECAST CHART
# =====================================================

def plot_forecast(
    historical_df,
    forecast_df
):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=historical_df["Date"],
            y=historical_df["Total"],
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

    if (
        "Upper" in forecast_df.columns
        and
        "Lower" in forecast_df.columns
    ):

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
                name="Confidence Interval"
            )
        )

    fig.update_layout(
        title="Traffic Forecast",
        template="plotly_white"
    )

    return fig


# =====================================================
# TRAFFIC DISTRIBUTION
# =====================================================

def plot_distribution(df):

    fig = px.histogram(
        df,
        x="Total",
        nbins=40,
        marginal="box",
        title="Traffic Distribution"
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig


# =====================================================
# TOP CONGESTION HOURS
# =====================================================

def plot_top_hours(df):

    top_hours = (
        df.groupby("Hour")["Total"]
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
        text_auto=".2f",
        title="Top 10 Congestion Hours"
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig
