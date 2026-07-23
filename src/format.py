from datetime import datetime

WEEKDAYS = ["月", "火", "水", "木", "金", "土", "日"]

def format_report_datetime(report_datetime: str):
    """取得日時を「xxxx年xx月xx日xx時」に変換する"""

    dt = datetime.fromisoformat(report_datetime)

    return f"{dt.year}年{dt.month}月{dt.day}日{dt.hour}時"


def format_forecast_date(forecast_date: str):
    """予報日を「xxxx年xx月xx日（x）」に変換する"""

    dt = datetime.fromisoformat(forecast_date)

    weekday = WEEKDAYS[dt.weekday()]

    return f"{dt.year}年{dt.month}月{dt.day}日（{weekday}）"


def format_weather(weather_info):
    return f"""明日の天気予報

明日の日付：{format_forecast_date(weather_info["forecast_date"])}
天気：{weather_info["weather_string"]}

降水確率
18〜24時：{weather_info["rain_18_24"]}%
00〜06時：{weather_info["rain_00_06"]}%
06〜12時：{weather_info["rain_06_12"]}%
12〜18時：{weather_info["rain_12_18"]}%

最高気温：{weather_info["temp_max"]}℃
最低気温：{weather_info["temp_min"]}℃

予報取得時間：{format_report_datetime(weather_info["report_datetime"])}"""