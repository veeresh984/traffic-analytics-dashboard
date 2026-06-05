import pandas as pd
import streamlit as st

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data(file_path="data/TrafficTwoMonth.csv"):
    """
    Load and preprocess traffic dataset.
    """

    df = pd.read_csv(file_path)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Date conversion
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    # Time conversion
    df["Time"] = pd.to_datetime(
        df["Time"],
        errors="coerce"
    )

    # Feature Engineering
    df["Hour"] = df["Time"].dt.hour
    df["Minute"] = df["Time"].dt.minute
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.month_name()
    df["Day"] = df["Date"].dt.day
    df["Year"] = df["Date"].dt.year

    # Weekend Flag
    df["Is_Weekend"] = df["Day of the week"].isin(
        ["Saturday", "Sunday"]
    )

    # Time Period Classification
    df["Time_Period"] = df["Hour"].apply(
        classify_time_period
    )

    return df


# =====================================================
# TIME PERIOD CLASSIFICATION
# =====================================================

def classify_time_period(hour):

    if 5 <= hour < 12:
        return "Morning"

    elif 12 <= hour < 17:
        return "Afternoon"

    elif 17 <= hour < 21:
        return "Evening"

    return "Night"


# =====================================================
# FILTER DATA
# =====================================================

def filter_data(
    df,
    selected_days=None,
    selected_traffic=None
):
    """
    Apply dashboard filters.
    """

    filtered_df = df.copy()

    if selected_days:
        filtered_df = filtered_df[
            filtered_df["Day of the week"]
            .isin(selected_days)
        ]

    if selected_traffic:
        filtered_df = filtered_df[
            filtered_df["Traffic Situation"]
            .isin(selected_traffic)
        ]

    return filtered_df


# =====================================================
# KPI SUMMARY
# =====================================================

def get_kpi_summary(df):

    return {
        "total_traffic":
            df["Total"].sum(),

        "average_traffic":
            round(df["Total"].mean(), 2),

        "max_traffic":
            df["Total"].max(),

        "min_traffic":
            df["Total"].min(),

        "records":
            len(df)
    }


# =====================================================
# VEHICLE SUMMARY
# =====================================================

def get_vehicle_summary(df):

    return pd.DataFrame({

        "Vehicle": [
            "Cars",
            "Bikes",
            "Buses",
            "Trucks"
        ],

        "Count": [

            df["CarCount"].sum(),
            df["BikeCount"].sum(),
            df["BusCount"].sum(),
            df["TruckCount"].sum()

        ]
    })


# =====================================================
# HOURLY TRAFFIC
# =====================================================

def get_hourly_traffic(df):

    return (
        df.groupby("Hour")["Total"]
        .mean()
        .reset_index()
    )


# =====================================================
# DAILY TRAFFIC
# =====================================================

def get_daily_traffic(df):

    return (
        df.groupby("Day of the week")["Total"]
        .mean()
        .reset_index()
    )


# =====================================================
# TRAFFIC SITUATION SUMMARY
# =====================================================

def get_traffic_situation(df):

    situation = (
        df["Traffic Situation"]
        .value_counts()
        .reset_index()
    )

    situation.columns = [
        "Traffic Situation",
        "Count"
    ]

    return situation


# =====================================================
# HEATMAP DATA
# =====================================================

def get_heatmap_data(df):

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

    return heatmap.pivot(
        index="Day of the week",
        columns="Hour",
        values="Total"
    )


# =====================================================
# CORRELATION MATRIX
# =====================================================

def get_correlation_matrix(df):

    cols = [
        "CarCount",
        "BikeCount",
        "BusCount",
        "TruckCount",
        "Total"
    ]

    return df[cols].corr()


# =====================================================
# PEAK HOUR
# =====================================================

def get_peak_hour(df):

    hourly = (
        df.groupby("Hour")["Total"]
        .mean()
    )

    peak_hour = hourly.idxmax()
    peak_value = hourly.max()

    return peak_hour, peak_value


# =====================================================
# BUSIEST DAY
# =====================================================

def get_busiest_day(df):

    return (
        df.groupby(
            "Day of the week"
        )["Total"]
        .mean()
        .idxmax()
    )


# =====================================================
# LEAST BUSY DAY
# =====================================================

def get_least_busy_day(df):

    return (
        df.groupby(
            "Day of the week"
        )["Total"]
        .mean()
        .idxmin()
    )


# =====================================================
# DAILY SERIES FOR FORECASTING
# =====================================================

def get_forecast_series(df):

    return (
        df.groupby("Date")["Total"]
        .mean()
        .sort_index()
    )


# =====================================================
# SUMMARY STATISTICS
# =====================================================

def get_summary_statistics(df):

    return df[
        [
            "CarCount",
            "BikeCount",
            "BusCount",
            "TruckCount",
            "Total"
        ]
    ].describe()
