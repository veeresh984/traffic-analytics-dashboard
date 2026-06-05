import pandas as pd


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
# LOWEST HOUR
# =====================================================

def get_lowest_hour(df):

    hourly = (
        df.groupby("Hour")["Total"]
        .mean()
    )

    low_hour = hourly.idxmin()
    low_value = hourly.min()

    return low_hour, low_value


# =====================================================
# BUSIEST DAY
# =====================================================

def get_busiest_day(df):

    return (
        df.groupby("Day of the week")
        ["Total"]
        .mean()
        .idxmax()
    )


# =====================================================
# LEAST BUSY DAY
# =====================================================

def get_least_busy_day(df):

    return (
        df.groupby("Day of the week")
        ["Total"]
        .mean()
        .idxmin()
    )


# =====================================================
# DOMINANT VEHICLE
# =====================================================

def get_dominant_vehicle(df):

    vehicle_totals = {

        "Cars": df["CarCount"].sum(),
        "Bikes": df["BikeCount"].sum(),
        "Buses": df["BusCount"].sum(),
        "Trucks": df["TruckCount"].sum()

    }

    return max(
        vehicle_totals,
        key=vehicle_totals.get
    )


# =====================================================
# LEAST COMMON VEHICLE
# =====================================================

def get_least_vehicle(df):

    vehicle_totals = {

        "Cars": df["CarCount"].sum(),
        "Bikes": df["BikeCount"].sum(),
        "Buses": df["BusCount"].sum(),
        "Trucks": df["TruckCount"].sum()

    }

    return min(
        vehicle_totals,
        key=vehicle_totals.get
    )


# =====================================================
# TRAFFIC SITUATION SUMMARY
# =====================================================

def get_traffic_situation_summary(df):

    traffic_counts = (
        df["Traffic Situation"]
        .value_counts()
        .to_dict()
    )

    return traffic_counts


# =====================================================
# VEHICLE CONTRIBUTION %
# =====================================================

def get_vehicle_contribution(df):

    total = (
        df["CarCount"].sum()
        + df["BikeCount"].sum()
        + df["BusCount"].sum()
        + df["TruckCount"].sum()
    )

    contribution = {

        "Cars":
            round(
                (df["CarCount"].sum() / total) * 100,
                2
            ),

        "Bikes":
            round(
                (df["BikeCount"].sum() / total) * 100,
                2
            ),

        "Buses":
            round(
                (df["BusCount"].sum() / total) * 100,
                2
            ),

        "Trucks":
            round(
                (df["TruckCount"].sum() / total) * 100,
                2
            )
    }

    return contribution


# =====================================================
# TRAFFIC GROWTH
# =====================================================

def get_traffic_growth(df):

    daily = (
        df.groupby("Date")
        ["Total"]
        .mean()
        .reset_index()
        .sort_values("Date")
    )

    first_day = daily["Total"].iloc[0]
    last_day = daily["Total"].iloc[-1]

    growth = (
        (last_day - first_day)
        / first_day
    ) * 100

    return round(growth, 2)


# =====================================================
# CONGESTION SCORE
# =====================================================

def get_congestion_score(df):

    avg_traffic = df["Total"].mean()

    if avg_traffic < 40:
        return "Low"

    elif avg_traffic < 60:
        return "Moderate"

    elif avg_traffic < 80:
        return "High"

    else:
        return "Severe"


# =====================================================
# PEAK VEHICLE HOURS
# =====================================================

def get_peak_vehicle_hours(df):

    return {

        "Cars":
        df.groupby("Hour")
        ["CarCount"]
        .mean()
        .idxmax(),

        "Bikes":
        df.groupby("Hour")
        ["BikeCount"]
        .mean()
        .idxmax(),

        "Buses":
        df.groupby("Hour")
        ["BusCount"]
        .mean()
        .idxmax(),

        "Trucks":
        df.groupby("Hour")
        ["TruckCount"]
        .mean()
        .idxmax()

    }


# =====================================================
# SUMMARY CARD DATA
# =====================================================

def get_summary_insights(df):

    peak_hour, peak_value = get_peak_hour(df)

    low_hour, low_value = get_lowest_hour(df)

    return {

        "total_traffic":
            int(df["Total"].sum()),

        "average_traffic":
            round(
                df["Total"].mean(),
                2
            ),

        "maximum_traffic":
            int(df["Total"].max()),

        "minimum_traffic":
            int(df["Total"].min()),

        "peak_hour":
            peak_hour,

        "peak_hour_volume":
            round(
                peak_value,
                2
            ),

        "low_hour":
            low_hour,

        "low_hour_volume":
            round(
                low_value,
                2
            ),

        "busiest_day":
            get_busiest_day(df),

        "least_busy_day":
            get_least_busy_day(df),

        "dominant_vehicle":
            get_dominant_vehicle(df),

        "least_vehicle":
            get_least_vehicle(df),

        "traffic_growth":
            get_traffic_growth(df),

        "congestion_score":
            get_congestion_score(df)

    }


# =====================================================
# EXECUTIVE INSIGHT TEXT
# =====================================================

def generate_executive_insights(df):

    insights = get_summary_insights(df)

    return f"""
Peak traffic occurs at {insights['peak_hour']}:00
with an average volume of
{insights['peak_hour_volume']:.2f} vehicles.

The busiest day is {insights['busiest_day']}
while the least busy day is
{insights['least_busy_day']}.

The dominant vehicle category is
{insights['dominant_vehicle']}.

Traffic growth over the analysis period
is {insights['traffic_growth']}%.

Overall congestion level is classified as
{insights['congestion_score']}.
"""
