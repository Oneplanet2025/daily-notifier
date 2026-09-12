from datetime import datetime, timedelta
from src.providers.weather_json_models import WeatherInfo


WEEKDAYS = ["月", "火", "水", "木", "金", "土", "日"]


def format_report_datetime(report_datetime: str) -> str:
    """取得日時を「xxxx年xx月xx日xx時」に変換する"""

    dt = datetime.fromisoformat(report_datetime)

    return f"{dt.year}年{dt.month}月{dt.day}日{dt.hour}時"


def format_forecast_date(forecast_date: str) -> str:
    """予報日を「xxxx年xx月xx日（x）」に変換する"""

    dt = datetime.fromisoformat(forecast_date)

    weekday = WEEKDAYS[dt.weekday()]

    return f"{dt.year}年{dt.month}月{dt.day}日（{weekday}）"


def format_pop_datetime(forecast_date: str) -> str:
    """降水確率の日時を「xx月xx日xx時～xx時」に変換する"""

    start = datetime.fromisoformat(forecast_date)
    end = start + timedelta(hours=6)

    return f"{start.month}月{start.day}日{start.hour:02}時～{end.hour:02}時"


def format_weather_section(weather_info: WeatherInfo) -> str:
    pop_text = ""

    for rain in weather_info.rain_forecasts:
        pop_text += f"{format_pop_datetime(rain.time)}：{rain.probability}%\n"
    return f"""阪神の明日の天気予報

明日の日付：{format_forecast_date(weather_info.forecast_date)}
天気：{weather_info.weather}

降水確率：
{pop_text}

最高気温：{weather_info.temperature.maximum_temperature}℃
最低気温：{weather_info.temperature.minimum_temperature}℃

予報取得時間：{format_report_datetime(weather_info.report_datetime)}"""
