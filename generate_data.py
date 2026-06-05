import pandas as pd
import numpy as np
from datetime import datetime

# -----------------------------------------------------
# CONFIG
# -----------------------------------------------------

start_date = "2022-10-01"
end_date = "2022-11-30"

dates = pd.date_range(start_date, end_date, freq="D")

rows = []

# -----------------------------------------------------
# TRAFFIC GENERATOR
# -----------------------------------------------------

for date in dates:

    day_name = date.day_name()

    for hour in range(24):

        for minute in [0, 15, 30, 45]:

            time_str = f"{hour:02d}:{minute:02d}:00"

            # Traffic profile

            if 6 <= hour <= 9:
                base = np.random.randint(120, 180)

            elif 17 <= hour <= 20:
                base = np.random.randint(140, 220)

            elif 10 <= hour <= 16:
                base = np.random.randint(70, 130)

            elif 21 <= hour <= 23:
                base = np.random.randint(40, 80)

            else:
                base = np.random.randint(20, 60)

            # Vehicle split

            car = int(base * np.random.uniform(0.45, 0.55))
            bike = int(base * np.random.uniform(0.20, 0.30))
            bus = int(base * np.random.uniform(0.05, 0.10))

            truck = (
                base
                - car
                - bike
                - bus
            )

            total = (
                car
                + bike
                + bus
                + truck
            )

            # Traffic Label

            if total < 40:
                situation = "Low"

            elif total < 80:
                situation = "Normal"

            elif total < 130:
                situation = "High"

            else:
                situation = "Heavy"

            rows.append([
                time_str,
                date.strftime("%Y-%m-%d"),
                day_name,
                car,
                bike,
                bus,
                truck,
                total,
                situation
            ])

# -----------------------------------------------------
# CREATE DATAFRAME
# -----------------------------------------------------

df = pd.DataFrame(
    rows,
    columns=[
        "Time",
        "Date",
        "Day of the week",
        "CarCount",
        "BikeCount",
        "BusCount",
        "TruckCount",
        "Total",
        "Traffic Situation"
    ]
)

# -----------------------------------------------------
# SAVE CSV
# -----------------------------------------------------

df.to_csv(
    "TrafficTwoMonth.csv",
    index=False
)

print(df.shape)
print(df.head())
