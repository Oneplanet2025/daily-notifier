import requests

from src.config import (
    JMA_FORECAST_AREA_NAME,
    JMA_FORECAST_URL,
    JMA_TEMPERATURE_AREA_NAME,
)
from src.providers.weather_json_models import (
    RainForecast,
    TemperatureInfo,
    WeatherInfo,
)


def fetch_forecast_json():
    """気象庁から気象予報JSONを取得する"""

    response = requests.get(JMA_FORECAST_URL)
    response.raise_for_status()

    weather_json_data = response.json()

    return weather_json_data


def extract_weather_info(weather_json_data) -> WeatherInfo:
    """気象予報JSONから必要な情報だけ辞書として返す"""

    forecast_series = weather_json_data[0]["timeSeries"][0]
    pop_series = weather_json_data[0]["timeSeries"][1]
    temperature_series = weather_json_data[0]["timeSeries"][2]

    # 東部の天気予報を取得
    forecast_area = find_area(
        forecast_series["areas"],
        JMA_FORECAST_AREA_NAME,
        "天気予報",
    )

    # 東部の降水確率を取得
    forecast_pop_area = find_area(
        pop_series["areas"],
        JMA_FORECAST_AREA_NAME,
        "降水確率",
    )

    forecast_pop_times = pop_series["timeDefines"]
    forecast_pops = forecast_pop_area["pops"]
    rain_forecasts: list[RainForecast] = []

    for forecast_time, pop in zip(forecast_pop_times, forecast_pops):
        rain_forecasts.append(
            RainForecast(
                time=forecast_time,
                probability=pop,
            )
        )

    # 名古屋の気温を取得
    temperature_area = find_area(
        temperature_series["areas"],
        JMA_TEMPERATURE_AREA_NAME,
        "気温情報",
    )

    temperature = TemperatureInfo(
        minimum_temperature=temperature_area["temps"][-2],
        maximum_temperature=temperature_area["temps"][-1],
    )

    weather_info = WeatherInfo(
        report_datetime=weather_json_data[0]["reportDatetime"],
        forecast_date=forecast_series["timeDefines"][1],
        weather=forecast_area["weathers"][1],
        rain_forecasts=tuple(rain_forecasts),
        temperature=temperature,
    )

    return weather_info


def find_area(areas, area_name: str, data_name: str):
    """指定された地域のデータを取得する"""

    for area in areas:
        if area["area"]["name"] == area_name:
            return area

    raise ValueError(f"{area_name} の{data_name}が見つかりません。")
