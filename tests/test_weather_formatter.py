import pytest

from src.providers.weather_json_models import (
    RainForecast,
    TemperatureInfo,
    WeatherInfo,
)
from src.formatters.weather_formatter import (
    format_forecast_date,
    format_pop_datetime,
    format_report_datetime,
    format_weather_section,
)


def test_format_report_datetime():
    result = format_report_datetime("2026-09-03T15:30:00+09:00")
    assert result == "2026年9月3日15時"

def test_format_report_datetime_invalid():
    with pytest.raises(ValueError):
        format_report_datetime("invalid-date")

def test_format_report_datetime_empty_string():
    with pytest.raises(ValueError):
        format_report_datetime("")

def test_format_report_datetime_none():
    with pytest.raises(TypeError):
        format_report_datetime(None)


def test_format_forecast_date():
    result = format_forecast_date("2026-09-04T00:00:00+09:00")
    assert result == "2026年9月4日（金）"

def test_format_forecast_date_invalid():
    with pytest.raises(ValueError):
        format_forecast_date("invalid-date")

def test_format_forecast_date_empty_string():
    with pytest.raises(ValueError):
        format_forecast_date("")

def test_format_forecast_date_none():
    with pytest.raises(TypeError):
        format_forecast_date(None)


def test_format_pop_datetime():
    result = format_pop_datetime("2026-09-04T00:00:00+09:00")
    assert result == "9月4日00時～06時"

def test_format_pop_datetime_evening():
    result = format_pop_datetime("2026-09-04T18:00:00+09:00")

    assert result == "9月4日18時～00時"

def test_format_pop_datetime_invalid():
    with pytest.raises(ValueError):
        format_pop_datetime("invalid-date")

def test_format_pop_datetime_empty_string():
    with pytest.raises(ValueError):
        format_pop_datetime("")

def test_format_pop_datetime_none():
    with pytest.raises(TypeError):
        format_pop_datetime(None)


def test_format_weather_section():
    weather_info = WeatherInfo(
        report_datetime="2026-09-03T15:30:00+09:00",
        forecast_date="2026-09-04T00:00:00+09:00",
        weather="晴れ",
        rain_forecasts=[
            RainForecast(
                time="2026-09-04T00:00:00+09:00",
                probability=20,
            ),
            RainForecast(
                time="2026-09-04T06:00:00+09:00",
                probability=30,
            ),
        ],
        temperature=TemperatureInfo(
            maximum_temperature=30,
            minimum_temperature=22,
        ),
    )

    result = format_weather_section(weather_info)

    assert "明日の天気予報" in result
    assert "明日の日付：2026年9月4日（金）" in result
    assert "天気：晴れ" in result
    assert "9月4日00時～06時：20%" in result
    assert "9月4日06時～12時：30%" in result
    assert "最高気温：30℃" in result
    assert "最低気温：22℃" in result
    assert "予報取得時間：2026年9月3日15時" in result