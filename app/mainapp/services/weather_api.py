import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry


def get_weather(coordinates):
    """
    Получение почасовой погоды по координатам на высоте 2 метра над уровнем моря
    """
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": coordinates['geo_lat'],
        "longitude": coordinates['geo_lon'],
        "elevation": 2,
        "hourly": "temperature_2m",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        ),
        "temperature_2m": hourly_temperature_2m,
    }

    hourly_dataframe = pd.DataFrame(data=hourly_data)

    data_dict = pd.DataFrame(hourly_dataframe).to_dict()

    date = []
    temp = []

    for i in data_dict['date'].values():
        date.append(i)

    for j in data_dict['temperature_2m'].values():
        j_round = round(j, 2)
        temp.append(j_round)

    result_dict = dict(zip(date, temp))

    return result_dict
