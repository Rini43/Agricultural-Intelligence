import requests
import pandas as pd
import time


def get_weather(
    latitude,
    longitude,
    start_date,
    end_date
):

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,

        "daily": [
            "temperature_2m_mean",
            "temperature_2m_max",
            "temperature_2m_min",
            "rain_sum",
            "relative_humidity_2m_mean"
        ],

        "timezone": "auto"
    }

    response = requests.get(
        url,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    return response.json()


def process_weather(data):

    daily = data["daily"]

    df = pd.DataFrame({
        "date": daily["time"],
        "temperature": daily[
            "temperature_2m_mean"
        ],
        "max_temperature": daily[
            "temperature_2m_max"
        ],
        "min_temperature": daily[
            "temperature_2m_min"
        ],
        "rainfall": daily[
            "rain_sum"
        ],
        "humidity": daily[
            "relative_humidity_2m_mean"
        ]
    })

    df["date"] = pd.to_datetime(
        df["date"]
    )

    df["Year"] = df["date"].dt.year

    return df


def aggregate_weather(df):

    result = df.groupby("Year").agg(

        Rainfall=(
            "rainfall",
            "sum"
        ),

        AvgTemperature=(
            "temperature",
            "mean"
        ),

        MaxTemperature=(
            "max_temperature",
            "max"
        ),

        AvgHumidity=(
            "humidity",
            "mean"
        ),

        RainyDays=(
            "rainfall",
            lambda x: (x > 1).sum()
        )

    ).reset_index()

    return result


if __name__ == "__main__":

    # Example: Thrissur
    latitude = 10.52
    longitude = 76.21

    data = get_weather(
        latitude,
        longitude,
        "2010-01-01",
        "2023-12-31"
    )

    daily = process_weather(data)

    yearly = aggregate_weather(daily)

    yearly.to_csv(
        "data/raw/weather_thrissur.csv",
        index=False
    )

    print(yearly)

