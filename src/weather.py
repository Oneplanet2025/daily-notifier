import requests
from src.config import JMA_FORECAST_URL, JMA_FORECAST_AREA_NAME,JMA_TEMPERATURE_AREA_NAME

def fetch_forecast_json():
    """気象庁から気象予報JSONを取得する"""

    response = requests.get(JMA_FORECAST_URL)
    response.raise_for_status()

    weather_json_data = response.json()

    return weather_json_data

def get_weather(weather_json_data):
    """気象予報JSONから必要な情報だけ辞書として返す"""

    # 東部の天気予報を取得
    forecast_area = None
    for area in weather_json_data[0]["timeSeries"][0]["areas"]:
        if area["area"]["name"] == JMA_FORECAST_AREA_NAME:
            forecast_area = area
            break
    if forecast_area is None:
        raise ValueError(f"{JMA_FORECAST_AREA_NAME} が見つかりません。")

    # 東部の降水確率を取得
    forecast_pop_area = None
    for area in weather_json_data[0]["timeSeries"][1]["areas"]:
        if area["area"]["name"] == JMA_FORECAST_AREA_NAME:
            forecast_pop_area = area
            break
    if forecast_pop_area is None:
        raise ValueError(f"{JMA_FORECAST_AREA_NAME} の降水確率が見つかりません。")


    # 名古屋の気温を取得
    temperature_area = None
    for area in weather_json_data[0]["timeSeries"][2]["areas"]:
        if area["area"]["name"] == JMA_TEMPERATURE_AREA_NAME:
            temperature_area = area
            break
    if temperature_area is None:
        raise ValueError(f"{JMA_TEMPERATURE_AREA_NAME} の気温情報が見つかりません。")

    weather_info = {
        "report_datetime": weather_json_data[0]["reportDatetime"],
        "forecast_date": weather_json_data[0]["timeSeries"][0]["timeDefines"][1],
        "weather_string":  forecast_area["weathers"][1],
        "rain_18_24":forecast_pop_area["pops"][1],
        "rain_00_06":forecast_pop_area["pops"][2],
        "rain_06_12":forecast_pop_area["pops"][3],
        "rain_12_18":forecast_pop_area["pops"][4],
        "temp_min": temperature_area["temps"][2],
        "temp_max": temperature_area["temps"][3],
    }

    return weather_info

